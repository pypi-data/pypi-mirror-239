from datetime import datetime
from tqdm import tqdm

import os
import requests
import mimetypes
import zipfile
import logging
import subprocess
import re
import urllib.parse as urlparse

# Custom imports
from .custom_logger import CustomLogger
from .attributes import AttributeDict

class DMSUpload:
    """
    A class used for downloading and uploading files to a DMS server.

    Attributes
    ----------
    username : str
        The username for the DMS server.
    password : str
        The password for the DMS server.
    dmsUrl : str
        The URL of the DMS server.
    path : str
        The path to save the downloaded file.
    zip : bool
        A flag to indicate whether to zip the downloaded file.
    enableLog : bool
        A flag to indicate whether to enable logging.
    logLevel : int
        The logging level.
    downloadPath : str
        The path to save the downloaded file.
    filename : str
        The name of the downloaded file.

    Methods
    -------
    upload_to_dms(link)
        Uploads a file to the DMS server.
    download_file(url)
        Downloads a file from a URL.
    zip_file(fileName, extension)
        Zips a file.
    """
    def __init__(self,options = {"username": None, 
           "password":None, 
           "dmsUrl": "", 
           "zip": True, 
           "path":None,
           "logLevel":logging.INFO, 
           "filename":None}):
        
        options = AttributeDict(options)
        
        self.username = options.username
        self.password = options.password
        if len(options.dmsUrl) > 0 and options.dmsUrl[-1] != "/":
            options.dmsUrl += "/"
        self.dmsUrl = options.dmsUrl
        self.path = options.path
        self.zip = options.zip
        self.enableLog = options.enableLog
        self.filename = options.filename
        self.loggingLevel = options.logLevel
        self.log = logging.getLogger("logger")
        self.log.setLevel(self.loggingLevel)
        success_level = logging.getLevelName("SUCCESS")
        if type(success_level) != int:
            CustomLogger.addLoggingLevel('SUCCESS', logging.INFO + 1)
        if self.loggingLevel == logging.DEBUG:
            logFormatter = CustomLogger(debug=True)
        else:
            logFormatter = CustomLogger()
        self.formatter = logFormatter  # remove parentheses here
        self.stdout_handler = logging.StreamHandler()
        self.stdout_handler.setLevel(self.loggingLevel)
        self.stdout_handler.setFormatter(self.formatter)
        self.log.addHandler(self.stdout_handler)
        self.log.propagate = False

    def filename_from_url(self,url):
        """:return: detected filename or None"""
        fname = os.path.basename(urlparse.urlparse(url).path)
        if len(fname.strip(" \n\t.")) == 0:
            return None
        return fname
    
    def filename_from_headers(self,headers):
        """Detect filename from Content-Disposition headers if present.
        http://greenbytes.de/tech/tc2231/

        :param: headers as dict, list or string
        :return: filename from content-disposition header or None
        """
        if type(headers) == str:
            headers = headers.splitlines()
        if type(headers) == list:
            headers = dict([x.split(':', 1) for x in headers])
        cdisp = headers.get("Content-Disposition")
        if not cdisp:
            return None
        cdtype = cdisp.split(';')
        if len(cdtype) == 1:
            return None
        if cdtype[0].strip().lower() not in ('inline', 'attachment'):
            return None
        # several filename params is illegal, but just in case
        fnames = [x for x in cdtype[1:] if x.strip().startswith('filename=')]
        if len(fnames) > 1:
            return None
        name = fnames[0].split('=')[1].strip(' \t"')
        name = os.path.basename(name)
        if not name:
            return None
        return name

    def upload_file(self, filePath):
        # Create a progress bar
        progress = tqdm(total=100, unit="Mb", unit_scale=True, desc="Uploading", dynamic_ncols=True)
        extension = filePath.split(".")[-1]
        # Execute the curl command
        if self.filename != None:
            filename = f"{self.filename}_{datetime.now().timestamp()}"
            self.dmsUrl += f"{filename}.{extension}"
        try:
            cmd = [
                "curl",
                "-T", filePath,
                self.dmsUrl,
                "-u", f"{self.username}:{self.password}",
                "--output", "/dev/stdout",
                "--progress-bar",
            ]

            process = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1, universal_newlines=True)

            while True:
                line = process.stderr.readline()
                if not line:
                    break

                match = re.search(r'\d+(\.\d+)?%', line)
                if match:
                    progress.update(float(match.group()[:-1]) - progress.n)

            process.wait()
            progress.close()

            if process.returncode == 0:
                self.log.success("Upload complete.")
                return True
            else:
                self.log.error(f"Upload failed with return code {process.returncode}")
                return False
        except Exception as e:
            self.log.error(f"An error occurred: {str(e)}")
            return False
        
    def __valid_zip(self, flePath):
        try:
            the_zip_file = zipfile.ZipFile(flePath)
            ret = the_zip_file.testzip()
            if ret is not None:
                self.log.error(f"First bad file in zip: {ret}")
                return False
        except Exception as ex:
            self.log.error(f"Exception: {ex}")
            return False
        
        self.log.success("Valid zip file")
        return True

    def upload_to_dms(self,link):
        """
        Uploads a file to the DMS server.

        Parameters
        ----------
        link : str
            The URL of the file to upload.

        Returns
        -------
        bool
            True if the upload was successful, False otherwise.
        """
        self.log.info("Starting Download...")
        
        fileURL = link
        stat, filename, extension = self.download_file(fileURL)
        fileName = filename.split(".")[0:-1]
        fileName = ".".join(fileName)
        self.log.debug(f"File Name: {fileName}")
        self.log.debug(f"File Extension: {extension}")

        if stat == 1:
            if self.zip:
                if self.zip_file(fileName, extension):
                    if self.__valid_zip(f"{fileName}.zip") == False:
                        self.log.error("Invalid zip file")
                        return False
                    else:
                        filepath = f"{fileName}.zip"
                else:   
                    self.log.error("Zip Failed... Try Again...")
                    return False
            else:
                filepath = filename

            upload_status = self.upload_file(filepath)

            if upload_status:
                self.log.success("Upload Finished...")
                return True
            else:
                self.log.error("Upload Failed... Try Again...")
        else:
            self.log.error("Upload Failed...")
            return False
        
    def download_file(self, url):
        """
        Downloads a file from a URL.

        Parameters
        ----------
        url : str
            The URL of the file to download.

        Returns
        -------
        tuple
            A tuple containing the status of the download (1 for success, 0 for failure), the name of the downloaded file, and the file extension.
        """
        # Streaming, so we can iterate over the response.
        response = requests.get(url, stream=True)
        total_size_in_bytes = int(response.headers.get('content-length', 0))
        filename = self.filename_from_url(url)
        filename2 = self.filename_from_headers(response.headers)

        extension = filename.split(".")[-1]

        if len(extension) > 4 and filename2 == None:
            self.log.debug("File extension from mimetypes")
            extension = mimetypes.guess_extension(
                str(response.headers.get("content-type", 0)))
            extension = extension.split(".")[-1]
            number = len([name for name in os.listdir('.') if os.path.isfile(name)])
            filename = f'{self.filename}_{number}_{datetime.now().timestamp()}.{extension}'

        elif filename2 == None:
            self.log.debug("File extension from url")
            extension = filename.split(".")[-1]
        else:
            self.log.debug("File extension from headers")
            extension = filename2.split(".")[-1]
            filename = filename2

        self.log.debug(f"File Name: {filename}")
        self.log.debug(f"File Extension: {extension}")
        
        block_size = 1024  # 1 Kibibyte
        # simple version for working with CWD
        
        progress_bar = tqdm(total=total_size_in_bytes, desc=f"Downloading", unit='iB', unit_scale=True)
        
        if self.path != None:
            filename = f'{self.path}/{filename}'

        with open(filename, 'wb') as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)

        progress_bar.close()

        filename = os.path.abspath(filename)
        self.log.debug(f"File saved to: {filename}")

        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
            self.log.error("something went wrong")
            return (0, None, None)
        else:
            self.log.success("Download Finished!")
            return (1, filename, extension)
        
    def zip_file(self, fileName, extension):
        """
        Zips a file.

        Parameters
        ----------
        fileName : str
            The name of the file to zip.
        extension : str
            The extension of the file to zip.
        """
        if extension != "zip":
            self.log.info("Zipping File...")
            try:
                with zipfile.ZipFile(f"{fileName}.zip", mode="w") as archive:
                    archive.write(f"{fileName}.{extension}")

                    if self.enableLog:
                        self.log.success(f"Zipping {fileName} Finished!")
                    else:
                        print(f"Zipping {fileName} Finished!")

                    return True
                
            except Exception as e:
                self.log.error(f"An error occurred: {str(e)}")
                return False
        else:
            self.log.info("File is already zipped...")
            return True



