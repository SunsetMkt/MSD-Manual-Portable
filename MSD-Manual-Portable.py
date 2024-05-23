#!/usr/env python3
# -*- coding: utf-8 -*-
# MSD-Manual-Portable
# A method to build a portable and offline-available MSD Manual.
# https://github.com/lwd-temp/MSD-Manual-Portable
#
# MSD-Manual-Portable.py
# Download, unpack the MSD Manual, copy HTML files to the portable folder and run a HTTP server.
import argparse
import base64
import hashlib
import http.server
import json
import os
import shutil
import socket
import sys
import threading
import time
import webbrowser
import zipfile

import requests
import tqdm


def resource_path(relative_path):
    """Get absolute path to resource, works for dev env and PyInstaller"""
    # HTML resources are packed in the executable and MSDProfessionalMedicalTopics.zip should be placed in where the executable is.
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(relative_path)


def get_filename(url):
    return os.path.basename(url)


def get_filename_noext(filename):
    return os.path.splitext(filename)[0]


def check_port_available(port):
    # Check if port is available
    # If not, try to use port +1, +2, ...
    print("Checking port {}...".format(port))
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(("localhost", port))
            s.close()
            print("Port {} is available.".format(port))
            break
        except socket.error:
            print("Port {} is not available. Trying next one...".format(port))
            port += 1
    return port


def httpd(PORT):
    httpd = http.server.HTTPServer(
        ("localhost", PORT), http.server.SimpleHTTPRequestHandler
    )
    return httpd.serve_forever()


def get_latest_version(version="professional", language="zh"):
    url = "https://api.merck.com/merck-manuals/v1/topicsyncdate"
    querystring = {"version": str(version), "language": str(language)}
    headers = {
        base64.b64decode("WC1NZXJjay1BUElLZXk=")
        .decode("utf-8"): base64.b64decode(
            "VVZ6NGI0dDRON3pjT0wyMGh2VVpNc1o5dU1mUzZqYXg="
        )
        .decode("utf-8")
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()["TopicSyncDate"]


def short_hash(string):
    return hashlib.sha256(string.encode("utf-8")).hexdigest()[:5]


def construct_filename(version="professional", language="zh"):
    if language == "en":
        language = ""
    else:
        language = language.upper()

    version = version[0].upper() + version[1:]

    # MSDZHProfessionalMedicalTopics.zip
    return f"MSD{language}{version}MedicalTopics.zip"


def stream_download(url, path):
    r = requests.get(url, stream=True)
    with open(path, "wb") as f:
        try:
            total_length = int(r.headers.get("content-length"))
        except:
            total_length = None
        # tqdm
        for chunk in tqdm.tqdm(
            r.iter_content(chunk_size=1024),
            total=total_length / 1024 + 1,
            desc=get_filename(url),
        ):
            if chunk:
                f.write(chunk)
                f.flush()
    print(f"Download complete: {url}")
    return path


def simple_download(url, path):
    r = requests.get(url)
    with open(path, "wb") as f:
        f.write(r.content)
    print(f"Download complete: {url}")
    return path


def compact_dumps(obj):
    return json.dumps(obj, separators=(",", ":"), indent=None)


def load_json(path):
    return json.load(open(path, encoding="utf-8-sig"))


def msd_manual_parser(target_dir, dest_dir):
    # Get curr version
    print("Getting current version...")
    try:
        curr_version = get_latest_version()
    except:
        curr_version = "unknown"
    # Save to jsonp
    with open(
        os.path.join(dest_dir, "version_portable.js"), "w", encoding="utf-8"
    ) as f:
        f.write(f"version_callback({compact_dumps(curr_version)})")

    # Generate index
    print("Generating index...")
    index = load_json(os.path.join(target_dir, "Json", "sections.json"))
    for section in index["sections"]:
        chapters = load_json(
            os.path.join(target_dir, "Json", section["SectionId"] + ".json")
        )
        section["chapters"] = chapters["chapters"]
    # Save to jsonp
    with open(os.path.join(dest_dir, "index_portable.js"), "w", encoding="utf-8") as f:
        f.write(f"index_callback({compact_dumps(index)})")

    # Generate searchcontent
    print("Generating searchcontent...")
    searchcontent = load_json(os.path.join(target_dir, "Json", "searchcontent.json"))
    # Save to jsonp
    with open(
        os.path.join(dest_dir, "searchcontent_portable.js"), "w", encoding="utf-8"
    ) as f:
        f.write(f"searchcontent_callback({compact_dumps(searchcontent)})")

    if not args.vet:
        # Generate Pearls.json
        print("Generating pearls...")
        pearls = load_json(os.path.join(target_dir, "Json", "Pearls.json"))
        # Save to jsonp
        with open(
            os.path.join(dest_dir, "pearls_portable.js"), "w", encoding="utf-8"
        ) as f:
            f.write(f"pearls_callback({compact_dumps(pearls)})")

    return dest_dir


# argparse
parser = argparse.ArgumentParser(
    # prog='MSD-Manual-Portable',
    description="Host a portable and offline-available MSD Manual.",
    epilog="https://github.com/lwd-temp/MSD-Manual-Portable",
)
# lang: en zh
parser.add_argument(
    "-l",
    "--lang",
    default="zh",
    choices=["en", "zh"],
    help="Language of the MSD Manual.",
)
# version: professional consumer
parser.add_argument(
    "-v",
    "--version",
    default="professional",
    choices=["professional", "consumer"],
    help="Version of the MSD Manual.",
)
# port: 1-65535 integer, default: PORT
parser.add_argument(
    "-p",
    "--port",
    default=33914,  # 33914 is the first five digits of "MSD"'s SHA-256 hash
    type=int,
    help="Port of the HTTP Server, 1-65535.",
)
# silent: do not do anything after building
parser.add_argument(
    "-s",
    "--silent",
    action="store_true",
    help="Do not do anything after building.",
)
# vet: download the vet version MSDVetMedicalTopics.zip
parser.add_argument(
    "--vet",
    action="store_true",
    help="Download the vet version (English only) and ignore version and lang argument.",
)
args = parser.parse_args()


# Download the MSD Manual

# Pre-Config
if not args.vet:
    zipURL = f"https://mmcdnprdcontent.azureedge.net/{construct_filename(args.version, args.lang)}"
else:
    # zipURL = f"https://mmcdnprdvet.azureedge.net/{construct_filename('vet', args.lang)}"  # MSDVetMedicalTopics.zip
    zipURL = "https://mmcdnprdcontent.azureedge.net/MSDVetMedicalTopics.zip"
origFilename = get_filename(zipURL)
pureFilename = get_filename_noext(origFilename)
tmpFilename = f"{origFilename}.tmp"
unzippedDirName = pureFilename

if not (
    os.path.exists(origFilename)
    or os.path.exists(os.path.join("unzippedDirName", "index.html"))
):
    print("Downloading MSD Manual...")
    downloadedPath = stream_download(zipURL, tmpFilename)
    # Rename the downloaded file
    os.rename(downloadedPath, origFilename)
else:
    print("MSD Manual already downloaded.")


if not os.path.exists(os.path.join(unzippedDirName, "index.html")):
    print("Unpacking MSD Manual...")
    with zipfile.ZipFile(origFilename, "r") as zip_ref:
        zip_ref.extractall(unzippedDirName)
    print("Unpacking complete.")

    # Try getting favicon.ico
    favicon = "https://www.msdmanuals.com/favicon.ico"
    print("Downloading favicon.ico...")
    try:
        simple_download(favicon, resource_path(os.path.join("HTML", "favicon.ico")))
    except:
        pass

    msd_manual_parser(unzippedDirName, resource_path("HTML"))

    # Copy index files to the folder
    print("Copying index files to the folder...")
    # Copy all files in HTML folder to the folder
    for file in os.listdir(resource_path("HTML")):
        shutil.copy(resource_path(os.path.join("HTML", file)), unzippedDirName)
    print("Copying complete.")
else:
    print("MSD Manual already unpacked.")

if args.silent:
    sys.exit()

# Change the current working directory to the folder
os.chdir(unzippedDirName)


# Run the HTTP server
print("Starting the HTTP server...")

# Start server and open browser
PORT = check_port_available(args.port)
server = threading.Thread(target=httpd, args=(PORT,), daemon=True)
server.start()
print(f"The HTTP server is running on localhost:{PORT}...")
print(f"You can now open the MSD Manual in your browser at http://localhost:{PORT}/")
print("Press Ctrl+C to stop the server.")

webbrowser.open(f"http://localhost:{PORT}")

# Ctrl+C to exit
try:
    while True:
        time.sleep(100)  # sleep to avoid performance issues
except KeyboardInterrupt:
    sys.exit()
