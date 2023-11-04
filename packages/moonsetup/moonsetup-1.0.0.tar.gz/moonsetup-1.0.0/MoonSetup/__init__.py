import os
import requests
import zipfile
import tempfile

from MoonUtils import generaterandomstring

class Downloader:
    @staticmethod
    def DownloadFiles(url):
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            temp_dir = tempfile.gettempdir()
            temp_file = os.path.join(temp_dir, generaterandomstring() + ".zip")

            with open(temp_file, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

            with zipfile.ZipFile(temp_file, 'r') as zip_ref:
                zip_ref.extractall(os.path.dirname(__file__))
        except (requests.exceptions.RequestException, zipfile.BadZipFile, Exception) as e:
            print(f"[MoonSetup] Failed to download/extract file: {e}")

class VersionChecker:
    @staticmethod
    def CheckVersion(version, url):
        versionfromurl = requests.get(url).text
        if version == versionfromurl:
            return True
        else:
            return False

