#!/usr/env python3
# -*- coding: utf-8 -*-
# MSD-Manual-Portable
# A method to build a portable and offline-available MSD Manual.
# https://github.com/lwd-temp/MSD-Manual-Portable
#
# start.py
# Download, unpack the MSD Manual, copy HTML files to the portable folder and run a HTTP server.
import http.server
import os
import shutil
import sys
import threading
import time
import webbrowser
import zipfile

import requests
from clint.textui import progress


def getFilename(url):
    return url.split('/')[-1]


def getFilenameWithoutExtension(filename):
    return filename.split('.')[0]


def httpd(PORT):
    httpd = http.server.HTTPServer(
        ('localhost', PORT), http.server.SimpleHTTPRequestHandler)
    httpd.serve_forever()


# Default HTTP Server Port for fallback.
PORT = 16771  # 16771 is the first five digits of MSD's SHA-1 hash


# Get system arguments: blank/zh/en
if len(sys.argv) == 1:
    language = 'zh'
elif len(sys.argv) == 2:
    language = sys.argv[1]
else:
    print('Usage: python start.py [zh/en]')
    sys.exit(1)
# If not zh or en
if language != 'zh' and language != 'en':
    print("Undefined language: " + language)
    print('Usage: python start.py [zh/en]')
    sys.exit(1)

# Download the MSD Manual
if language == 'zh':
    url = "https://mmcdnprdcontent.azureedge.net/MSDZHProfessionalMedicalTopics.zip"
    PORT = 16771
elif language == 'en':
    url = "https://mmcdnprdcontent.azureedge.net/MSDProfessionalMedicalTopics.zip"
    PORT = 16772  # Add 1 to avoid collision with zh
else:
    # Fallback to zh
    print("Undefined language, fallback to zh.")
    url = "https://mmcdnprdcontent.azureedge.net/MSDZHProfessionalMedicalTopics.zip"
    PORT = 16771

if not (os.path.exists(getFilename(url)) or os.path.exists(getFilenameWithoutExtension(getFilename(url)))):
    print("Downloading MSD Manual...")
    r = requests.get(url, stream=True)
    path = getFilename(url)+'.tmp'
    with open(path, 'wb') as f:
        total_length = int(r.headers.get('content-length'))
        for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
            if chunk:
                f.write(chunk)
                f.flush()
    print("Download complete.")
    # Rename the downloaded file
    os.rename(path, getFilename(url))

    # Try getting favicon.ico
    favicon = "https://www.msdmanuals.com/favicon.ico"
    print("Downloading favicon.ico...")
    try:
        r = requests.get(favicon)
        with open(os.path.join("HTML", "favicon.ico"), "wb") as f:
            f.write(r.content)
        print("Download complete.")
    except:
        print("Failed to get favicon.ico.")
        print("This is not necessarily a problem.")
        pass

else:
    print("MSD Manual already downloaded.")


if not os.path.exists(getFilenameWithoutExtension(getFilename(url))):
    # Unpack the MSD Manual to MSDZHProfessionalMedicalTopics folder
    path = getFilename(url)
    print("Unpacking MSD Manual...")
    with zipfile.ZipFile(path, 'r') as zip_ref:
        zip_ref.extractall(getFilenameWithoutExtension(getFilename(url)))
    print("Unpacking complete.")
    print(getFilename(url) +
          " can be removed manually without affecting the portable MSD Manual.")

    # Copy the HTML files to the folder
    print("Copying HTML files to the folder...")
    # Copy all files in HTML folder to the folder
    for file in os.listdir('HTML'):
        shutil.copy(os.path.join('HTML', file),
                    getFilenameWithoutExtension(getFilename(url)))
    print("Copying complete.")
else:
    print("MSD Manual already unpacked.")


# Change the current working directory to the folder
print("Changing the current working directory to " +
      getFilenameWithoutExtension(getFilename(url))+"...")
os.chdir(getFilenameWithoutExtension(getFilename(url)))


# Run the HTTP server
print("Starting the HTTP server...")

# Start server and open browser
server = threading.Thread(target=httpd, args=(PORT,))
server.daemon = True
server.start()
print("The HTTP server is running on localhost:"+str(PORT)+"...")
print("You can now open the MSD Manual in your browser at http://localhost:"+str(PORT)+"/")
print("Press Ctrl+C to stop the server.")
webbrowser.open('http://localhost:' + str(PORT))

# Ctrl+C to stop the server
try:
    while True:
        time.sleep(100)  # sleep to avoid performance issues
except KeyboardInterrupt:
    sys.exit()
except Exception as e:
    print(e)
    sys.exit()
finally:
    sys.exit()
