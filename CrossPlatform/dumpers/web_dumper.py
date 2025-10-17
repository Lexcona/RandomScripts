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

skip_domain_check = args.skip_domain_check

def extract_domain(url:str, subdomain:bool=True):
    funny2 = url.split("://")[-1].split("/")[0]
    if not subdomain:
        thing = funny2.split(".")
        funny2 = thing[-2]+"."+thing[-1]
    return funny2


def download_page(url:str):
    console.print("Grabbing: " + url, style="cyan")
    try:
        res = session.get(url, timeout=10)
    except:
        return
    #path = urlparse(url).path
    path = url.split("://")[-1]
    if path.endswith("/") or path == "":
        path += "index.html"
    if not "." in path.split("/")[-1]:
        path += ".html"
    if formated:
        ext = path.split("?")[0].split('.')[-1].lower()
        matched_folder = "others"
        for folder, extensions in types_to_files.items():
            if ext in [e.lower() for e in extensions]:
                matched_folder = folder
                break

        output_thing = os.path.join(
            output,
            extract_domain(path),
            matched_folder,
            urlparse(url).path.lstrip("/")
        )
    else:
        output_thing = os.path.join(output, path.lstrip("/")).split("?")[0]


    os.makedirs(os.path.dirname(output_thing), exist_ok=True)
    try:
        soup = BeautifulSoup(res.content, "html.parser")
        if soup.find_all("html") == []:
            if not os.path.exists(output_thing):
                console.print("Downloading: " + output_thing, style="cyan")
                with open(output_thing, "wb") as f:
                    f.write(res.content)
                console.print("Downloaded: " + output_thing, style="green")
            else:
                console.print("Skipped (exists): " + output_thing, style="red")
        else:
            if skip_domain_check or extract_domain(url, False) == extract_domain(urlBase, False):
                for tag in tags:
                    for mm in soup.find_all(tag):
                        src = mm.get("src")
                        href = mm.get("href")
                        if src:
                            gotten_urls.append(urljoin(url, src))
                        if href:
                            gotten_urls.append(urljoin(url, href))
            
            if not os.path.exists(output_thing):
                console.print("Downloading: " + output_thing, style="cyan")
                with open(output_thing, "wb") as f:
                    f.write(res.content)
                console.print("Downloaded: " + output_thing, style="green")
            else:
                console.print("Skipped (exists): " + output_thing, style="red")
    except:
        if not os.path.exists(output_thing):
            console.print("Downloading: " + output_thing, style="cyan")
            with open(output_thing, "wb") as f:
                f.write(res.content)
            console.print("Downloaded: " + output_thing, style="green")
        else:
            console.print("Skipped (exists): " + output_thing, style="red")

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
