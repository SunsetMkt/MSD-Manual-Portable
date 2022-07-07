# MSD-Manual-Portable
# A method to build a portable and offline-available MSD Manual.
# https://github.com/lwd-temp/MSD-Manual-Portable
#
# Get and unzip the MSD Manual.
#
import zipfile

import requests

url = "https://mmcdnprdcontent.azureedge.net/MSDZHProfessionalMedicalTopics.zip"


def getzip():
    print("Downloading MSDZHProfessionalMedicalTopics.zip")
    r = requests.get(url)
    with open("MSDZHProfessionalMedicalTopics.zip", "wb") as f:
        f.write(r.content)
    print("Downloaded MSDZHProfessionalMedicalTopics.zip")


def unzip():
    # Unzip to MSDZHProfessionalMedicalTopics folder
    print("Unzipping MSDZHProfessionalMedicalTopics.zip")
    with zipfile.ZipFile("MSDZHProfessionalMedicalTopics.zip", "r") as zip_ref:
        zip_ref.extractall("MSDZHProfessionalMedicalTopics")
    print("Unzipped MSDZHProfessionalMedicalTopics.zip")


def main():
    getzip()
    unzip()
    print("Done!")


if __name__ == "__main__":
    main()
