import os
import random
import urllib
import urllib3
import argparse
import requests
import threading

from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from rich.console import Console

parser = argparse.ArgumentParser()
parser.add_argument("url")
parser.add_argument("-o", "--output")
parser.add_argument("-fi", "--filter")
parser.add_argument("-e", "--exclude")
parser.add_argument("-f", "--formated", action="store_true")
parser.add_argument("-d", "--skip-domain-check", action="store_true")
parser.add_argument("-t", "--threads", default=200)
args = parser.parse_args()

urlBase = args.url
session = requests.session()
session.headers["User-Agent"] = random.choice(requests.get("https://gist.githubusercontent.com/pzb/b4b6f57144aea7827ae4/raw/cf847b76a142955b1410c8bcef3aabe221a63db1/user-agents.txt").text.splitlines())
gotten_urls = []
visited = set()
threads = []
console = Console()

tags = ["img", "video", "a", "link", "script"]

types_to_files = {
    "css": ["css"],
    "html": ["html"],
    "javascript": ["js"],
    "img": [
        "ase",
        "art",
        "bmp",
        "blp",
        "cd5",
        "cit",
        "cpt",
        "cr2",
        "cut",
        "dds",
        "dib",
        "djvu",
        "egt",
        "exif",
        "gif",
        "gpl",
        "grf",
        "icns",
        "ico",
        "iff",
        "jng",
        "jpeg",
        "jpg",
        "jfif",
        "jp2",
        "jps",
        "lbm",
        "max",
        "miff",
        "mng",
        "msp",
        "nef",
        "nitf",
        "ota",
        "pbm",
        "pc1",
        "pc2",
        "pc3",
        "pcf",
        "pcx",
        "pdn",
        "pgm",
        "PI1",
        "PI2",
        "PI3",
        "pict",
        "pct",
        "pnm",
        "pns",
        "ppm",
        "psb",
        "psd",
        "pdd",
        "psp",
        "px",
        "pxm",
        "pxr",
        "qfx",
        "raw",
        "rle",
        "sct",
        "sgi",
        "rgb",
        "int",
        "bw",
        "tga",
        "tiff",
        "tif",
        "vtf",
        "xbm",
        "xcf",
        "xpm",
        "3dv",
        "amf",
        "ai",
        "awg",
        "cgm",
        "cdr",
        "cmx",
        "dxf",
        "e2d",
        "egt",
        "eps",
        "fs",
        "gbr",
        "odg",
        "svg",
        "stl",
        "vrml",
        "x3d",
        "sxd",
        "v2d",
        "vnd",
        "wmf",
        "emf",
        "art",
        "xar",
        "png",
        "webp",
        "jxr",
        "hdp",
        "wdp",
        "cur",
        "ecw",
        "iff",
        "lbm",
        "liff",
        "nrrd",
        "pam",
        "pcx",
        "pgf",
        "sgi",
        "rgb",
        "rgba",
        "bw",
        "int",
        "inta",
        "sid",
        "ras",
        "sun",
        "tga",
        "heic",
        "heif"
    ],
    "video": [
        "webm",
        "mkv",
        "flv",
        "vob",
        "ogv",
        "ogg",
        "rrc",
        "gifv",
        "mng",
        "mov",
        "avi",
        "qt",
        "wmv",
        "yuv",
        "rm",
        "asf",
        "amv",
        "mp4",
        "m4p",
        "m4v",
        "mpg",
        "mp2",
        "mpeg",
        "mpe",
        "mpv",
        "m4v",
        "svi",
        "3gp",
        "3g2",
        "mxf",
        "roq",
        "nsv",
        "flv",
        "f4v",
        "f4p",
        "f4a",
        "f4b",
        "mod"
    ],
    "audio": [
        "aac",
        "aiff",
        "ape",
        "au",
        "flac",
        "gsm",
        "it",
        "m3u",
        "m4a",
        "mid",
        "mod",
        "mp3",
        "mpa",
        "ogg",
        "pls",
        "ra",
        "s3m",
        "sid",
        "wav",
        "wma",
        "xm"
    ],
    "executables": [
        "exe",
        "msi",
        "bin",
        "command",
        "sh",
        "bat",
        "crx",
        "bash",
        "csh",
        "fish",
        "ksh",
        "zsh"
    ],
    "fonts": [
        "eot",
        "otf",
        "ttf",
        "woff",
        "woff2"
    ],
    "archivrs": [
        "7z",
        "a",
        "aar",
        "apk",
        "ar",
        "bz2",
        "br",
        "cab",
        "cpio",
        "deb",
        "dmg",
        "egg",
        "gz",
        "iso",
        "jar",
        "lha",
        "lz",
        "lz4",
        "lzma",
        "lzo",
        "mar",
        "pea",
        "rar",
        "rpm",
        "s7z",
        "shar",
        "tar",
        "tbz2",
        "tgz",
        "tlz",
        "txz",
        "war",
        "whl",
        "xpi",
        "zip",
        "zipx",
        "zst",
        "xz",
        "pak"
    ],
    "scripts":[
        "ada",
        "adb",
        "ads",
        "asm",
        "asp",
        "aspx",
        "bas",
        "bash",
        "bat",
        "cpp",
        "c",
        "cbl",
        "cc",
        "class",
        "clj",
        "cob",
        "cpp",
        "cs",
        "csh",
        "cxx",
        "d",
        "diff",
        "dll",
        "e",
        "el",
        "f",
        "f77",
        "f90",
        "fish",
        "for",
        "fth",
        "ftn",
        "go",
        "groovy",
        "h",
        "hh",
        "hpp",
        "hs",
        "htm",
        "html",
        "hxx",
        "inc",
        "java",
        "js",
        "json",
        "jsp",
        "jsx",
        "ksh",
        "kt",
        "kts",
        "lhs",
        "lisp",
        "lua",
        "m",
        "m4",
        "nim",
        "patch",
        "php",
        "php3",
        "php4",
        "php5",
        "phtml",
        "pl",
        "po",
        "pp",
        "prql",
        "py",
        "ps1",
        "psd1",
        "psm1",
        "ps1xml",
        "psc1",
        "pssc",
        "psrc",
        "r",
        "rb",
        "rs",
        "s",
        "scala",
        "sh",
        "sql",
        "swg",
        "swift",
        "v",
        "vb",
        "vcxproj",
        "wll",
        "xcodeproj",
        "xml",
        "xll",
        "zig",
        "zsh"
    ],
    "documents": [
        "doc",
        "docx",
        "ebook",
        "log",
        "md",
        "msg",
        "odt",
        "org",
        "pages",
        "pdf",
        "rtf",
        "rst",
        "tex",
        "txt",
        "wpd",
        "wps"
    ]
}

max_threads = int(args.threads)
if args.output:
    output = args.output
else:
    output = urlBase.split("://")[-1].split("/")[0]

if args.formated:
    formated = True
else:
    formated = False

if args.filter:
    filterr = args.filter.replace(" ").split(",")
else:
    filterr = []

if args.exclude:
    exclude = args.exclude.replace(" ").split(",")
else:
    exclude = []

skip_domain_check = args.skip_domain_check

def download_thing(data, output:str):
    if filterr != []:
        if not output.split(".")[-1].replace("/", "") in filterr:
            return
    
    if exclude != []:
        if output.split(".")[-1].replace("/", "") in exclude:
            return

    if not os.path.exists(output):
        console.print("Downloading: " + output, style="cyan")
        with open(output, "wb") as f:
            f.write(data)
        console.print("Downloaded: " + output, style="green")
    else:
        console.print("Skipped (exists): " + output, style="red")

def extract_domain(url:str, subdomain:bool=True):
    funny2 = url.split("://")[-1].split("/")[0]
    if not subdomain:
        thing = funny2.split(".")
        funny2 = thing[-2]+"."+thing[-1]
    return funny2


def download_page(url: str):
    console.print("Grabbing: " + url, style="cyan")
    res = session.get(url)

    parsed = urlparse(url)
    domain = parsed.netloc
    path = parsed.path

    if path == "" or path.endswith("/"):
        path = os.path.join(path, "index.html")

    elif not os.path.splitext(path)[1]:
        path = path + ".html"

    clean_path = path.lstrip("/")

    if formated:
        matched_folder = "others"
        for folder, extensions in types_to_files.items():
            if os.path.splitext(clean_path.split("?")[0])[1].lstrip(".").lower() in extensions:
                matched_folder = folder
                break

        output_thing = os.path.join(
            output,
            domain,
            matched_folder,
            clean_path
        )
    else:
        output_thing = os.path.join(output, domain, clean_path).split("?")[0]

    os.makedirs(os.path.dirname(output_thing), exist_ok=True)

    try:
        soup = BeautifulSoup(res.content, "html.parser")

        if soup.find_all("html") != []:
            if skip_domain_check or extract_domain(url, False) == extract_domain(urlBase, False):
                for mm in soup.find_all():
                    src = mm.get("src")
                    href = mm.get("href")
                    if src:
                        gotten_urls.append(urljoin(url, src))
                        console.print("Queueing: "+urljoin(url, src), style="cyan")
                    if href:
                        gotten_urls.append(urljoin(url, href))
                        console.print("Queueing: "+urljoin(url, href), style="cyan")

    except Exception as e:
        console.print("None HTML found: " + output_thing, style="cyan")
    download_thing(res.content, output_thing)

download_page(urlBase)

while gotten_urls:
    url = gotten_urls.pop(0)
    if url in visited:
        continue
    visited.add(url)
    if len(threads) < max_threads:
        thread = threading.Thread(target=download_page, args=(url,))
        thread.start()
        threads.append(thread)
    else:
        console.print("Waiting for threads to finish...", style="yellow")
        for thread in threads:
            thread.join()
        threads = []

for thread in threads:
    thread.join()
threads = []
