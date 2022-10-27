#!/usr/env python3
# -*- coding: utf-8 -*-
# MSD-Manual-Portable
# A method to build a portable and offline-available MSD Manual.
# https://github.com/lwd-temp/MSD-Manual-Portable
#
# MSD-Manual-Portable.py
# Download, unpack the MSD Manual, copy HTML files to the portable folder and run a HTTP server.
import argparse
import http.server
import os
import shutil
import socket
import sys
import threading
import time
import webbrowser
import zipfile

import requests
from clint.textui import progress


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    # This is how should MSD-Manual-Portable.py work with Pyinstaller:
    # HTML resources are packed in the executable and MSDProfessionalMedicalTopics.zip should be placed in where the executable is.

    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(relative_path)


def getFilename(url):
    return url.split('/')[-1]


def getFilenameWithoutExtension(filename):
    return filename.split('.')[0]


def check_port_available(port):
    # Check if port is available
    # If not, try to use port +1, +2, ...
    print('Checking port {}...'.format(port))
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(('localhost', port))
            s.close()
            print('Port {} is available.'.format(port))
            break
        except socket.error:
            print('Port {} is not available. Trying next one...'.format(port))
            port += 1
    return port


def httpd(PORT):
    httpd = http.server.HTTPServer(
        ('localhost', PORT), http.server.SimpleHTTPRequestHandler)
    httpd.serve_forever()


# Default HTTP Server Port for fallback.
DEFPORT = 33914  # 33914 is the first five digits of MSD's SHA-256 hash


# argparse
parser = argparse.ArgumentParser(
    # prog='MSD-Manual-Portable',
    description='Host a portable and offline-available MSD Manual.',
    epilog='https://github.com/lwd-temp/MSD-Manual-Portable')
# lang: en zh
parser.add_argument('-l', '--lang', default='zh',
                    choices=['en', 'zh'], help='Language of the MSD Manual. Default: zh')
# version: professional consumer
parser.add_argument('-v', '--version', default='professional', choices=[
                    'professional', 'consumer'], help='Version of the MSD Manual. Default: professional')
# port: any integer, default: PORT
parser.add_argument('-p', '--port', default=DEFPORT, type=int,
                    help='Port of the HTTP Server. Default port changes for different languages and versions.')
# silent: do not open browser
parser.add_argument('-s', '--silent', action='store_true',
                    help='Do not open browser.')

args = parser.parse_args()

# Set PORT
PORT = args.port

# Download the MSD Manual
baseURL = "https://mmcdnprdcontent.azureedge.net/"
if args.version == 'professional':
    if args.lang == 'en':
        filename = 'MSDProfessionalMedicalTopics.zip'
        if PORT == DEFPORT:
            PORT = DEFPORT
    else:
        filename = 'MSDZHProfessionalMedicalTopics.zip'
        if PORT == DEFPORT:
            PORT = DEFPORT + 100
elif args.version == 'consumer':
    if args.lang == 'en':
        filename = 'MSDConsumerMedicalTopics.zip'
        if PORT == DEFPORT:
            PORT = DEFPORT + 200
    else:
        filename = 'MSDZHConsumerMedicalTopics.zip'
        if PORT == DEFPORT:
            PORT = DEFPORT + 300
else:
    print('Error: Invalid version.')
    sys.exit(1)

url = baseURL + filename

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
        with open(resource_path(os.path.join("HTML", "favicon.ico")), "wb") as f:
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
    for file in os.listdir(resource_path('HTML')):
        shutil.copy(resource_path(os.path.join('HTML', file)),
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
PORT = check_port_available(PORT)
server = threading.Thread(target=httpd, args=(PORT,))
server.daemon = True
server.start()
print("The HTTP server is running on localhost:"+str(PORT)+"...")
print("You can now open the MSD Manual in your browser at http://localhost:"+str(PORT)+"/")
print("Press Ctrl+C to stop the server.")
if not args.silent:
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
