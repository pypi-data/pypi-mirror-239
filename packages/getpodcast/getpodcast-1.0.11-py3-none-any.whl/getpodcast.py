#! /usr/bin/env python3

import argparse
import collections
import datetime
import email.utils
import mimetypes
import os
import re
import shutil
import socket
import sys
import urllib.error
import urllib.request

from pyPodcastParser.Podcast import Item, Podcast

__version__ = "1.0.11"

mimetypes.init()

# options tuple
Options = collections.namedtuple(
    "Options",
    [
        "run",
        "dryrun",
        "onlynew",
        "deleteold",
        "quiet",
        "list",
        "keywords",
        "podcast",
        "date_from",
        "root_dir",
        "template",
        "user_agent",
        "hooks",
    ],
)

# Global for the message function
quiet = False


def options(**kwargs) -> Options:
    """
    Calls the `argparse.ArgumentParser` and add the result into a
    `Options` object. Default values is collected from ``kwargs`` but
    values from `~argparse.ArgumentParser` takes precedence over ``kwargs``.

    :param kwargs: default values if no value is found in `~argparse.ArgumentParser`

    Usage example:

    .. code-block:: py
        :linenos:

        import getpodcast

        opt = getpodcast.options(
            date_from='2022-01-01',
            root_dir='./podcast')

        podcasts = {
            "SGU": "https://feed.theskepticsguide.org/feed/sgu"
        }

        getpodcast.getpodcast(podcasts, opt)
    """
    parser = argparse.ArgumentParser(
        description="Download podcasts.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    default_template = "{rootdir}/{podcast}/{year}/{date} {title}{ext}"

    parser.add_argument(
        "--run",
        action="store_true",
        default=kwargs.get("run", False),
        help="Download podcasts.",
    )
    parser.add_argument(
        "--dryrun",
        action="store_true",
        default=kwargs.get("dryrun", False),
        help="Test. Does not download podcasts.",
    )
    parser.add_argument(
        "--onlynew",
        action="store_true",
        default=kwargs.get("onlynew", False),
        help="Only process new entries.",
    )
    parser.add_argument(
        "--deleteold",
        action="store_true",
        default=kwargs.get("deleteold", False),
        help="Delete entries older than 'date_from' date.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        default=kwargs.get("quiet", False),
        help="Quiet mode (for cron jobs)",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        default=kwargs.get("list", False),
        help="List all podcasts",
    )
    parser.add_argument(
        "--keywords",
        action="store_true",
        default=kwargs.get("keywords", False),
        help="List available keywords for filename template",
    )
    parser.add_argument(
        "--template",
        default=kwargs.get("template", default_template),
        help="Filename template",
    )
    parser.add_argument(
        "--podcast",
        default=kwargs.get("podcast", ""),
        help="Only process this podcast. default: all",
    )
    parser.add_argument(
        "--date-from",
        default=kwargs.get("date_from", "1970-01-01"),
        help="Only download podcast newer then date",
    )
    parser.add_argument(
        "--root-dir",
        default=kwargs.get("root_dir", "./podcast"),
        help="Podcast download directory",
    )
    parser.add_argument(
        "--user-agent",
        default=kwargs.get("user_agent", ""),
        help="web request identification",
    )
    parser.add_argument(
        "--hooks",
        default=kwargs.get("hooks", ""),
        help="comma separated key=value list of hooks",
    )

    args = parser.parse_args()

    # verify hooks
    try:
        list(parse_hooks_string(args.hooks))
    except ValueError:
        print("Error parsing hooks string. Expected format:")
        print("validated=funcname,preprocess=anotherfunc")
        raise SystemExit()

    opt = Options(**args.__dict__)

    global quiet
    quiet = opt.quiet

    # if missing argument print help
    if not any((opt.run, opt.dryrun, opt.list, opt.keywords)):
        parser.print_help()
    return opt


def getpodcast(podcasts: dict, args: Options) -> None:
    """
    Parses the podcasts and options and calls the `process_podcast`
    function for each podcast.
    """

    # print list of podcasts
    if args.list:
        for p in podcasts.keys():
            print(p)
        return

    # print list of keywords
    if args.keywords:
        for item in (
            ("rootdir", "base directory for downloads"),
            ("podcast", "key part of podcast dict"),
            ("date", "item publish date (format: YYYY.MM.DD)"),
            ("isodate", "item publish date (format: YYYY-MM-DD)"),
            ("title", "item title"),
            ("year", "item publish year (format: YYYY)"),
            ("month", "item publish month (format: MM)"),
            ("day", "item publish day (format: DD)"),
            ("ext", "enclosure file extension"),
            ("guid", "GUID of episode"),
        ):
            print("{%s} = %s" % item)
        return

    if not (args.run or args.dryrun):
        return

    headers = {}
    if args.user_agent:
        headers["User-Agent"] = args.user_agent

    fromdate = datetime.datetime.strptime(args.date_from, "%Y-%m-%d")

    for pod, url in podcasts.items():
        process_podcast(pod, url, headers, fromdate, args)


def process_podcast(
    pod: str, url: str, headers: dict, fromdate: datetime.datetime, args: Options
) -> None:
    """
    Fetches the RSS-feed for given podcast and calls the `process_podcast_item`
    function for each item found.
    """
    # if --podcast is used we will only process a matching name
    if args.podcast:
        if not args.podcast == pod:
            return  # continue

    try:
        request = urllib.request.Request(url, headers=headers)
        content = urllib.request.urlopen(request)
        podcast = Podcast(content.read())
    except (urllib.error.HTTPError, urllib.error.URLError) as err:
        message("Podcast: {}".format(pod), wait=True)
        message("Connection error: {}".format(err))
        return  # continue

    for item in podcast.items:
        try:
            process_podcast_item(pod, item, headers, fromdate, args)
        except SkipPodcast:
            break


class SkipPodcast(Exception):
    "Skip to the next podcast."
    pass


def process_podcast_item(
    pod: str, item: Item, headers: dict, fromdate: datetime.datetime, args: Options
) -> None:
    """
    Compares the many different properties given in `~pyPodcastParser.Item.Item` and `Options`.
    Will do one of the following based on the results:

    * Skip to next episode.
    * Delete episode if `Options.deleteold` is `True`.
    * Download and validate episode by calling `try_download_item` and
      `validateFile`.


    """
    # skip if date is older then --date-from and --deleteold isn't used
    if fromdate and not args.deleteold:
        if item.date_time < fromdate:
            return  # continue
    # skip if no audio
    if item.enclosure_url is None:
        return  # continue

    # create a dict with info to be used in filename
    data = {
        "rootdir": args.root_dir.rstrip("/"),
        "podcast": pod,
        "date": item.date_time.strftime("%Y.%m.%d"),
        "isodate": item.date_time.strftime("%Y-%m-%d"),
        "title": getSafeFilenameFromText(item.title.strip(" .")),  # scrub title
        "year": str(item.date_time.year),
        "month": "{:02d}".format(item.date_time.month),
        "day": "{:02d}".format(item.date_time.day),
        "guid": item.guid,
        "ext": parseFileExtensionFromUrl(item.enclosure_url)
        or mimetypes.guess_extension(item.enclosure_type),
    }

    filename_template = args.template
    newfilename = filename_template.format(**data)
    newfilelength = 0
    newfilemtime = item.time_published

    message(
        "\n".join(
            (
                "",
                "Podcast: {}",
                "  Date:  {}",
                "  Title: {}",
                "  File:  {}:",
                "  Status:",
            )
        ).format(pod, data["date"], data["title"], newfilename),
        wait=True,
    )

    # if file exist we check if filesize match with content length...
    if os.path.isfile(newfilename):
        # If the the date is older than date-from and deleteold is true, try to delete the file
        if fromdate and args.deleteold:
            if item.date_time < fromdate:
                if args.dryrun:
                    message("Pretending to delete file")
                else:
                    try:
                        os.remove(newfilename)
                        message("File deleted")
                    except OSError as error:
                        message("Error deleting old file")
                        message(error)
                return  # continue
        newfilelength = os.path.getsize(newfilename)
        try:
            if validateFile(
                newfilename,
                item.time_published,
                item.enclosure_length,
                item.enclosure_url,
                headers,
            ):
                if (
                    args.onlynew
                ):  # if file is valid and --onlynew is set then we jump to next podcast
                    raise SkipPodcast
                else:
                    return  # continue
        except (urllib.error.HTTPError, urllib.error.URLError):
            message("Connection when verifying existing file")
            return  # continue
        except socket.timeout:
            message("Connection timeout when downloading file")
            return  # continue

    # Stop if the date is older than date-from and deleteold is true
    if fromdate:
        if item.date_time < fromdate:
            return  # continue

    # use --dryrun to test parameter changes.
    if args.dryrun:
        if newfilelength:
            message("Pretending to resume from byte {}".format(newfilelength))
            return  # continue
        else:
            message("Pretending to download")
            return  # continue

    # download or resume podcast. retry if timeout. cancel if error
    cancel_validate, newfilelength = try_download_item(
        newfilelength, newfilename, item, headers
    )

    if cancel_validate:
        return  # continue

    # validate downloaded file
    try:
        if validateFile(
            newfilename, 0, item.enclosure_length, item.enclosure_url, headers
        ):
            # set mtime if validated
            os.utime(newfilename, (newfilemtime, newfilemtime))
            message("File validated")
            hooks(args.hooks, "validated", locals())

        elif newfilelength:
            # did not validate. see if we got same size as last time we
            # downloaded this file
            if newfilelength == os.path.getsize(newfilename):
                # ok, size is same. maybe data from response and rss is wrong.
                os.utime(newfilename, (newfilemtime, newfilemtime))
                message("File is assumed to be ok.")
    except urllib.error.HTTPError:
        message("Connection error when verifying download")
        return  # continue
    except socket.timeout:
        message("Connection timeout when downloading file")
        return  # continue


def try_download_item(newfilelength: int, newfilename: str, item: Item, headers: dict):
    """
    Try to download or resume an item by calling `downloadFile` or `resumeDownloadFile`.
    Retries download/resume on `socket.timeout`. Returns when connection fails,
    item is downloaded or no more data can be downloaded.

    :rtype: tuple[bool, int]

    :returns:
        * ``cancel_validate``: `True` if download was unsuccessful.
        * ``newfilelength``: File size of the download.
    """
    retry_downloading = True
    while retry_downloading:
        retry_downloading = False
        cancel_validate = False
        try:
            if newfilelength:
                resumeDownloadFile(newfilename, item.enclosure_url, headers)
            else:
                downloadFile(newfilename, item.enclosure_url, headers)
        except (urllib.error.HTTPError, urllib.error.URLError):
            message("Connection error when downloading file")
            cancel_validate = True
        except socket.timeout:
            if newfilelength:
                if os.path.getsize(newfilename) > newfilelength:
                    message("Connection timeout. File partly resumed. Retrying")
                    retry_downloading = True
                    newfilelength = os.path.getsize(newfilename)
                else:
                    message("Connection timeout when resuming file")
                    cancel_validate = True
            else:
                if os.path.isfile(newfilename):
                    newfilelength = os.path.getsize(newfilename)
                    if newfilelength > 0:
                        message("Connection timeout. File partly downloaded. Retrying")
                        retry_downloading = True
                    else:
                        message("Connection timeout when downloading file")
                        cancel_validate = True
                else:
                    message("Connection timeout when downloading file")
                    cancel_validate = True

    return cancel_validate, newfilelength


def downloadFile(newfilename: str, enclosure_url: str, headers: dict) -> None:
    """
    Download file from `enclosure_url` and store to `newfilename`. The timeout
    is set to 30sec. `shutil.copyfileobj` is used to store the file.
    """
    # create download dir path if it does not exist
    if not os.path.isdir(os.path.dirname(newfilename)):
        os.makedirs(os.path.dirname(newfilename))

    # download podcast
    message("Downloading ...")

    request = urllib.request.Request(enclosure_url, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        with open(newfilename, "wb") as out_file:
            shutil.copyfileobj(response, out_file, 100 * 1024)

    message("Download complete")


def resumeDownloadFile(newfilename: str, enclosure_url: str, headers: dict) -> None:
    """
    Compares the file size of `newfilename` and `Content-Length` from `headers`
    to determine if data is missing. Proceeds to download the missing data
    from `enclosure_url`. The timeout is set to 30sec. `shutil.copyfileobj`
    is used to store the file.
    """
    # find start-bye and total byte-length
    message("Prepare resume")
    request = urllib.request.Request(enclosure_url, headers=headers)
    with urllib.request.urlopen(request) as response:
        info = response.info()
        if "Content-Length" in info:
            contentlength = int(info["Content-Length"])
        else:
            contentlength = -1

    if os.path.isfile(newfilename):
        start_byte = os.path.getsize(newfilename)
    else:
        start_byte = 0

    request = urllib.request.Request(enclosure_url, headers=headers)
    if start_byte > 0:
        if start_byte >= contentlength:
            message("Resume not possible. (startbyte greater then contentlength)")
            return
        request.add_header("Range", "bytes={}-".format(start_byte))

    with urllib.request.urlopen(request, timeout=30) as response:
        with open(newfilename, "ab+") as out_file:
            info = response.info()
            out_file.seek(start_byte)

            if "Content-Range" in info:
                contentrange = info["Content-Range"].split(" ")[1].split("-")[0]
                if not int(contentrange) == start_byte:
                    message(
                        "Resume not possible. Cannot start download from byte {}".format(
                            start_byte
                        )
                    )
                    return

            if not out_file.tell() == start_byte:
                message(
                    "Resume not possible. Cannot append data from byte {}".format(
                        start_byte
                    )
                )
                return

            message("Start resume from byte {}".format(start_byte))
            message("Downloading ...")
            shutil.copyfileobj(response, out_file, 100 * 1024)

    message("Resume complete")


def validateFile(
    newfilename: str,
    time_published: int,
    enclosure_length: int,
    enclosure_url: str,
    headers: dict,
) -> bool:
    """
    Try to validate the file by looking at the file size and
    last modified time.
    """
    if os.path.isfile(newfilename + ".err"):
        return True  # skip file

    # try to validate size

    filelength = os.path.getsize(newfilename)
    if enclosure_length:
        if abs(filelength - enclosure_length) <= 1:
            return True
    else:
        enclosure_length = 0

    request = urllib.request.Request(enclosure_url, headers=headers)
    with urllib.request.urlopen(request) as response:
        info = response.info()
        if "Content-MD5" in info:
            message("Content-MD5:{}".format(info["Content-MD5"]))

        if "Content-Length" in info:
            contentlength = int(info["Content-Length"])
            if abs(filelength - contentlength) <= 1:
                return True
            elif filelength > contentlength:
                return True

        message(
            "{} filelength:{:,} enclosurelength:{:,} contentlength:{:,}".format(
                "Filelength and content-length mismatch.",
                filelength,
                enclosure_length,
                int(info.get("Content-Length", "0")),
            )
        )

        # if size validation fail, try to validate mtime.

        if time_published:
            filemtime = parseUnixTimeToDatetime(os.path.getmtime(newfilename))
            time_published = parseUnixTimeToDatetime(time_published)
            if time_published == filemtime:
                return True

            if "Last-Modified" in info:
                last_modified = parseRftTimeToDatetime(info["Last-Modified"])
                if last_modified == filemtime:
                    return True
            else:
                last_modified = ""

            message(
                "Last-Modified mismatch. file-mtime:{} Last-Modified:{} pubdate:{}".format(
                    filemtime, last_modified, time_published
                )
            )
    return False


def getSafeFilenameFromText(text: str) -> str:
    """
    Removes reserved system keywords from text.
    """
    # remove reserved windows keywords
    reserved_win_keywords = r"(PRN|AUX|CLOCK\$|NUL|CON|COM[1-9]|LPT[1-9])"

    # remove reserved windows characters
    reserved_win_chars = '[\x00-\x1f\\\\?*:";|/<>]'
    # reserved posix is included in reserved_win_chars. reserved_posix_characters = '/\0'

    extra_chars = "[$@{}]"

    tmp = re.sub(
        "|".join((reserved_win_keywords, reserved_win_chars, extra_chars)), "", text
    )
    return tmp


def parseFileExtensionFromUrl(enclosure_url: str) -> str:
    """
    Attempts to guess the correct file extension from the url.
    """
    return os.path.splitext(enclosure_url)[1].split("?")[0].lower().strip()


def parseRftTimeToDatetime(datetimestr: str) -> datetime.datetime:
    """
    This is a wrapper for `email.utils.parsedate_to_datetime`.
    Returns a UTC timestamp.
    """
    return email.utils.parsedate_to_datetime(datetimestr)


def parseUnixTimeToDatetime(datetimestamp: int) -> datetime.datetime:
    """
    This is a wrapper for `datetime.datetime.utcfromtimestamp`.
    Returns a UTC timestamp.
    """
    return datetime.datetime.utcfromtimestamp(datetimestamp)


messagebuffer = ""


def message(msg: str, wait: bool = False) -> None:
    """
    Print a message to the console. The message will be prefixed with
    8 blank spaces. If the special option ``wait`` is ``True`` the
    message will not be printed right away, it is instead stored in a
    message buffer. The message in the message buffer will not be
    prefixed with blank spaces:

    .. code-block:: pycon

        >>> def example():
        ...     message("Podcast: Some podcast", wait=True)
        ...     message("Downloading ...")
        ...     message("Downloading complete")
        ...     message("Verified")
        >>> example()
        Podcast: Some podcast
                 Downloading ...
                 Downloading complete
                 Verified
    """
    if quiet:
        return

    global messagebuffer
    if wait:
        messagebuffer = msg
        return

    if messagebuffer:
        print(messagebuffer)
        messagebuffer = ""

    print("        ", msg)


def parse_hooks_string(hooks: str):
    """
    Parse the hook-string from `~getpodcast.Options.hooks`.

    Expected formats:

    * A single hook: ``hookname=functionname``
    * Multiple hooks: ``hookname=functionname,hookname2=functionname2``

    :returns: A generator
    """
    if hooks:
        for hook in hooks.split(","):
            key, val = hook.split("=")
            yield key, val


def hooks(hook_string: str, hook_name: str, kwargs: dict):
    """
    Activate a hook.

    .. code-block:: pycon
        :caption: Example

        >>> hook_str = "validated=compressor"
        >>> def compressor(*args, **kwargs):
        ...     podcast = kwargs["pod"]
        ...     print(f"Activated for {podcast}")

        >>> def main():
        ...     pod = "somepodcast"
        ...     hooks(hook_str, "validated", locals())

        >>> main()
        Activated for somepodcast

    """
    for key, val in parse_hooks_string(hook_string):
        if key == hook_name:
            mod = sys.modules.get("__main__", __name__)
            if hasattr(mod, val):
                hook = getattr(mod, val)
                if callable(hook):
                    hook(**kwargs)
