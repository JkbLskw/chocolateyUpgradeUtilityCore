import re
import sys
from abc import ABCMeta, abstractmethod
from os import getcwd
from urllib.request import urlopen
from packages.version import Version
from helper.package_helper import PackageHelper
import logging
import datetime

class AbstractPackage(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.ONE_HUNDRET = 100
        self.temp_dir = getcwd() + "\\temp\\"
        self.temp_path = self.temp_dir
        self.chocolatey_url_pattern = r"https:\/\/chocolatey\.org\/api\/\w\d\/package\/.*"

    @abstractmethod
    def downloadlink(self):
        """download-link of package"""
        return

    @abstractmethod
    def chocolateylink(self):
        """chocolatey-link of package"""
        return

    @abstractmethod
    def packagepath(self):
        """absolute path of package"""
        return

    @abstractmethod
    def nuspec(self):
        """nuspec-file of package"""
        return

    @abstractmethod
    def installscript(self):
        """installscript of package"""
        return

    @abstractmethod
    def uninstallscript(self):
        """uninstallscript of package"""
        return

    def chocolatey_version(self, url):
        version_number = None
        if re.match(self.chocolatey_url_pattern, url):
            # reading version out of filename
            split_url = urlopen(url).geturl().split("/")
            filename = split_url[len(split_url) - 1]
            version_number = [int(x) for x in filename.split(".")[1:-1]]
        else:
            print("no valid chocolatey-package-url (pattern: " + self.chocolatey_url_pattern + ")")
        return version_number

    def progress(self, count, block_size, total_size):
        count_size = count * block_size
        percent = int(count_size * 100 / total_size)
        date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        sys.stdout.write("\r%s [%s] downloading... %d%%" % (date, type(self).__name__, percent))
        if percent is self.ONE_HUNDRET:
            sys.stdout.write("\r")
        sys.stdout.flush()

    def compare(self):
        """ compares versions of two files with given urls """
        self.temp_path = PackageHelper.download(self.downloadlink(), self.temp_path, self.progress)
        download_version = self.version(self.temp_path)
        chocolatey_version = self.chocolatey_version(self.chocolateylink())
        return Version(download_version, chocolatey_version)
