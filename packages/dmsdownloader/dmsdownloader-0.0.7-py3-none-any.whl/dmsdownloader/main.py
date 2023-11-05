
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

class DMSDownloader:
    def __init__(self,username=None, password=None, dmsUrl=None, path=None, zip=True, enableLog=False, logLevel=logging.DEBUG, downloadPath=None, filename="Matlab"):
        self.username = username
        self.password = password
        self.dmsUrl = dmsUrl
        self.path = path
        self.zip = zip
        self.enableLog = enableLog
        self.downloadPath = downloadPath
        self.filename = filename
        self.logLevel = logLevel
        if self.enableLog:
            self.logger = logging.getLogger("logger")
            self.logger.setLevel(self.logLevel)
            CustomFormatter.addLoggingLevel('SUCCESS', logging.INFO + 1)
            if self.logLevel == logging.DEBUG:
                logFormatter = CustomFormatter(debug=True)
            else:
                logFormatter = CustomFormatter()
            self.formatter = logFormatter()
            self.stdout_handler = logging.StreamHandler()
            self.stdout_handler.setLevel(self.logLevel)
            self.stdout_handler.setFormatter(self.formatter)
            self.logger.addHandler(self.stdout_handler)

    def upload_to_dms(self,link):
        if self.enableLog:
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
                        
            if self.enableLog:
                self.logger.success("Upload Finished... Deleting Cache...")
            else:
                print("Upload Finished... Deleting Cache...")

            os.remove(f"{fileName}.zip")
            return True
        else:
            if self.enableLog:
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
            if self.enableLog:
                self.logger.error("ERROR, something went wrong")
            else:
                print("ERROR, something went wrong")
            return (0, None, None)
        else:
            if self.enableLog:
                self.logger.success("Download Finished!")
            else:
                print("Download Finished!")
            return (1, fileName, extension)
        
    def zip_file(self, fileName, extension):
        if extension != ".zip":
            if self.enableLog:
                self.logger.info("Zipping File...")
            else:
                print("Zipping File...")

            with zipfile.ZipFile(f"{fileName}.zip", mode="w") as archive:
                archive.write(f"{fileName}{extension}")

            if self.enableLog:
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
            if self.enableLog:
                self.logger.info("File is already zipped...")
            else:
                print("File is already zipped...")

class format:
    def __init__(self):
        self.DEBUG = '\033[95m'
        self.BLUE = '\033[94m'
        self.INFO = '\033[96m'
        self.SUCCESS = '\033[92m'
        self.WARNING = '\033[93m'
        self.ERROR = '\033[91m'
        self.RESET = '\033[0m'
        self.CRITICAL = '\033[31;1m'

class CustomFormatter(logging.Formatter):

    def __init__(self,colored=True, debug=False):
        super().__init__()
        self.debug = debug
        self.coloring = format()
        if self.debug:
            line_func = ':[%(lineno)s:%(funcName)s]:'
        else:
            line_func = ':'
        self.fmt = '%(asctime)s'+line_func+'[%(levelname)s]:%(message)s'
        self.FORMATS = {
            logging.DEBUG:self.fmt,
            logging.INFO: self.fmt,
            logging.WARNING: self.fmt,
            logging.ERROR: self.fmt,
            logging.CRITICAL: self.fmt,
            logging.SUCCESS: self.fmt
        }
        if colored:
            self.FORMATS = {
            logging.DEBUG:'%(asctime)s'+line_func+self.coloring.DEBUG+'[%(levelname)s]'+self.coloring.RESET+':%(message)s',
            logging.INFO: '%(asctime)s'+line_func+self.coloring.INFO+'[%(levelname)s]'+self.coloring.RESET+':%(message)s',
            logging.WARNING: '%(asctime)s'+line_func+self.coloring.WARNING+'[%(levelname)s]'+self.coloring.RESET+':%(message)s',
            logging.ERROR: '%(asctime)s'+line_func+self.coloring.ERROR+'[%(levelname)s]'+self.coloring.RESET+':%(message)s',
            logging.CRITICAL: '%(asctime)s'+line_func+self.coloring.CRITICAL+'[%(levelname)s]'+self.coloring.RESET+':%(message)s',
            logging.SUCCESS: '%(asctime)s'+line_func+self.coloring.SUCCESS+'[%(levelname)s]'+self.coloring.RESET+':%(message)s'
        }
            
    def addLoggingLevel(levelName, levelNum, methodName=None):
        """
        Comprehensively adds a new logging level to the `logging` module and the
        currently configured logging class.

        `levelName` becomes an attribute of the `logging` module with the value
        `levelNum`. `methodName` becomes a convenience method for both `logging`
        itself and the class returned by `logging.getLoggerClass()` (usually just
        `logging.Logger`). If `methodName` is not specified, `levelName.lower()` is
        used.

        To avoid accidental clobberings of existing attributes, this method will
        raise an `AttributeError` if the level name is already an attribute of the
        `logging` module or if the method name is already present 

        Example
        -------
        >>> addLoggingLevel('TRACE', logging.DEBUG - 5)
        >>> logging.getLogger(__name__).setLevel("TRACE")
        >>> logging.getLogger(__name__).trace('that worked')
        >>> logging.trace('so did this')
        >>> logging.TRACE
        5

        """
        if not methodName:
            methodName = levelName.lower()

        if hasattr(logging, levelName):
            raise AttributeError('{} already defined in logging module'.format(levelName))
        if hasattr(logging, methodName):
            raise AttributeError('{} already defined in logging module'.format(methodName))
        if hasattr(logging.getLoggerClass(), methodName):
            raise AttributeError('{} already defined in logger class'.format(methodName))

        # This method was inspired by the answers to Stack Overflow post
        # http://stackoverflow.com/q/2183233/2988730, especially
        # http://stackoverflow.com/a/13638084/2988730
        def logForLevel(self, message, *args, **kwargs):
            if self.isEnabledFor(levelNum):
                self._log(levelNum, message, args, **kwargs)
        def logToRoot(message, *args, **kwargs):
            logging.log(levelNum, message, *args, **kwargs)

        logging.addLevelName(levelNum, levelName)
        setattr(logging, levelName, levelNum)
        setattr(logging.getLoggerClass(), methodName, logForLevel)
        setattr(logging, methodName, logToRoot)


    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt,"%Y-%m-%d %H:%M:%S")
        return formatter.format(record)
