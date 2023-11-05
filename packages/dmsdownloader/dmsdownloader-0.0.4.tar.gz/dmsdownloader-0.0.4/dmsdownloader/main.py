
from tqdm import tqdm
from tqdm.utils import CallbackIOWrapper
import requests
import mimetypes
from datetime import datetime
import os
import os.path
from requests.auth import HTTPBasicAuth
import zipfile
import logging

from .util import logFormatter

class DMSDownloader:
    def __init__(self,username=None, password=None, dmsUrl=None, path=None, zip=True, logging=False, logLevel=logging.DEBUG, downloadPath=None, filename="Matlab"):
        self.username = username
        self.password = password
        self.dmsUrl = dmsUrl
        self.path = path
        self.zip = zip
        self.logging = logging
        self.downloadPath = downloadPath
        self.filename = filename
        self.logLevel = logLevel
        if self.logging:
            self.logger = logging.getLogger("logger")
            self.logger.setLevel(self.logLevel)
            logFormatter.CustomFormatter.addLoggingLevel('SUCCESS', logging.INFO + 1)
            self.formatter = logFormatter()
            self.stdout_handler = logging.StreamHandler()
            self.stdout_handler.setLevel(self.logLevel)
            self.stdout_handler.setFormatter(self.formatter)
            self.logger.addHandler(self.stdout_handler)

    def upload_to_dms(self,link):
        if self.logging:
            self.logger.info("Starting Download...")
        else:
            print("Starting Download...")
        fileURL = link
        stat, fileName, extension = self.download_file(fileURL)
        if self.zip:
            self.zip_file(fileName, extension)

        if stat == 1:
            file_size = os.stat(fileName+extension).st_size
            webDav_url = f'{self.dmsUrl}{fileName}.zip'
            with open(f"{fileName}{extension}", "rb") as f:
                with tqdm(total=file_size, unit="B", unit_scale=True, unit_divisor=1024) as t:
                    wrapped_file = CallbackIOWrapper(t.update, f, "read")
                    try:
                        requests.put(webDav_url, data=wrapped_file,
                                auth=HTTPBasicAuth(self.username, self.password))
                    except:
                        requests.put(webDav_url, data=wrapped_file,
                                auth=HTTPBasicAuth(self.username, self.password))
                        
            if self.logging:
                self.logger.success("Upload Finished... Deleting Cache...")
            else:
                print("Upload Finished... Deleting Cache...")

            os.remove(f"{fileName}.zip")
            return True
        else:
            if self.logging:
                self.logger.error("Upload Failed...")
            else:
                print("Upload Failed...")
            return False
        
    def download_file(self, url):
        # Streaming, so we can iterate over the response.
        response = requests.get(url, stream=True)
        total_size_in_bytes = int(response.headers.get('content-length', 0))
        extension = mimetypes.guess_extension(
            str(response.headers.get("content-type", 0)))
        block_size = 1024  # 1 Kibibyte
        # simple version for working with CWD
        number = len([name for name in os.listdir('.') if os.path.isfile(name)])
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
        fileName = f'{self.filename}_{number}_{datetime.now().timestamp()}'
        if self.path != None:
            fileName = f'{self.path}/{fileName}'

        with open(f"{fileName+extension}", 'wb') as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
        progress_bar.close()
        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
            if self.logging:
                self.logger.error("ERROR, something went wrong")
            else:
                print("ERROR, something went wrong")
            return (0, None, None)
        else:
            if self.logging:
                self.logger.success("Download Finished!")
            else:
                print("Download Finished!")
            return (1, fileName, extension)
        
    def zip_file(self, fileName, extension):
        if extension != ".zip":
            if self.logging:
                self.logger.info("Zipping File...")
            else:
                print("Zipping File...")

            with zipfile.ZipFile(f"{fileName}.zip", mode="w") as archive:
                archive.write(f"{fileName}{extension}")

            if self.logging:
                self.logger.success(f"Zipping {fileName} Finished!")
                self.logger.info("Deleting Old File....")
                os.remove(f"{fileName}{extension}")
                self.logger.info("Deleted...")
            else:
                print(f"Zipping {fileName} Finished!")
                print("Deleting Old File....")
                os.remove(f"{fileName}{extension}")
                print("Deleted...")
        else:
            if self.logging:
                self.logger.info("File is already zipped...")
            else:
                print("File is already zipped...")