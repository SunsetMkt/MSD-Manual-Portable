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
import zipfile

import requests
from clint.textui import progress

# Download the MSD Manual
url = "https://mmcdnprdcontent.azureedge.net/MSDZHProfessionalMedicalTopics.zip"

if not (os.path.exists("MSDZHProfessionalMedicalTopics.zip") or os.path.exists("MSDZHProfessionalMedicalTopics")):
    print("Downloading MSD Manual...")
    r = requests.get(url, stream=True)
    path = 'MSDZHProfessionalMedicalTopics.zip.tmp'
    with open(path, 'wb') as f:
        total_length = int(r.headers.get('content-length'))
        for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
            if chunk:
                f.write(chunk)
                f.flush()
    print("Download complete.")
    # Rename the downloaded file
    os.rename(path, 'MSDZHProfessionalMedicalTopics.zip')
else:
    print("MSD Manual already downloaded.")


if not os.path.exists("MSDZHProfessionalMedicalTopics"):
    # Unpack the MSD Manual to MSDZHProfessionalMedicalTopics folder
    path = 'MSDZHProfessionalMedicalTopics.zip'
    print("Unpacking MSD Manual...")
    with zipfile.ZipFile(path, 'r') as zip_ref:
        zip_ref.extractall('MSDZHProfessionalMedicalTopics')
    print("Unpacking complete.")

    # Copy the HTML files to the folder
    print("Copying HTML files to the folder...")
    # Copy all files in HTML folder to the folder
    for file in os.listdir('HTML'):
        shutil.copy(os.path.join('HTML', file),
                    'MSDZHProfessionalMedicalTopics')
    print("Copying complete.")
else:
    print("MSD Manual already unpacked.")


# Change the current working directory to the folder
print("Changing the current working directory to MSDZHProfessionalMedicalTopics...")
os.chdir('MSDZHProfessionalMedicalTopics')


# Run the HTTP server
print("Starting the HTTP server...")
print("You can now open the MSD Manual in your browser at http://localhost:8080/")
print("The HTTP server is running on localhost:8080.")
print("Press Ctrl+C to stop the server.")
httpd = http.server.HTTPServer(
    ('localhost', 8080), http.server.SimpleHTTPRequestHandler)
httpd.serve_forever()
