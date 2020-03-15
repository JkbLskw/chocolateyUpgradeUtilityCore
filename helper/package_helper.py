import hashlib
import os
import shutil
import zipfile
from os import path, remove, mkdir, rmdir, listdir
from urllib.request import urlopen, urlretrieve


class PackageHelper(object):
    """ helper-class for chocolatey-packages """

    @staticmethod
    def checksum(temp_path, hashtype=hashlib.sha256):
        """ checksum of file with given path and hashtype
        :param temp_path: temp path of installer
        :param hashtype: type of hashing
        :return: hex digest of hash
        """
        hash256 = hashtype()
        with open(temp_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                hash256.update(byte_block)
        return hash256.hexdigest()

    @staticmethod
    def download(url, temp_path, progress_hook=None):
        if not path.exists(temp_path):
            mkdir(temp_path, 755)
        temp_path = temp_path + urlopen(url).geturl().split("/")[-1]
        # use of FancyURLopener -> https://stackoverflow.com/questions/1308542/how-to-catch-404-error-in-urllib-urlretrieve
        test, response = urlretrieve(url, temp_path, progress_hook)
        return temp_path

    @staticmethod
    def unzip(temp_path, executable_path):
        executable_temp_path = "\\".join(temp_path.rsplit("\\")[:-1])
        with zipfile.ZipFile(temp_path, 'r') as zip_file:
            zip_file.extract(executable_path, executable_temp_path)
        # '/' zu '\\' im executable_path
        executable_path = executable_path.replace(os.path.altsep, os.path.sep)
        return "\\".join([executable_temp_path, executable_path])

    @staticmethod
    def cleanup(temp_path, temp_dir):
        if path.exists(temp_path):
            remove(temp_path)
        if path.exists(temp_dir) and len(listdir(temp_dir)) == 0:
            rmdir(temp_dir)
