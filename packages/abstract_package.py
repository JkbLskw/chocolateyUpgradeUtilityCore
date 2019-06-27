import logging
import re
from abc import ABCMeta, abstractmethod
from progressbar import ProgressBar, Percentage, Bar, UnknownLength
from os import path, getcwd, remove, mkdir
from urllib.request import urlopen, urlretrieve
from packages.version import Version

class AbstractPackage(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.progressbar = None
        self.temp_path = getcwd() + "\\temp\\"
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

    def download(self, url):
        if not path.exists(self.temp_path):
            mkdir(self.temp_path, 755)
        self.temp_path = self.temp_path + urlopen(url).geturl().split("/")[-1]
        response = urlretrieve(url, self.temp_path, reporthook=self.download_progress)
        return self.temp_path

    def download_progress(self, count, blocksize, totalsize):
        if self.progressbar is None:
            self.progressbar = ProgressBar(maxval=totalsize, widgets=[Percentage(), Bar()])
        self.progressbar.update(int(count * blocksize * 100 / totalsize))

    def cleanup(self):
        if path.exists(self.temp_path):
            remove(self.temp_path)

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

    def compare(self):
        """ compares versions of two files with given urls """
        a = self.version(self.download(self.downloadlink()))
        b = self.chocolatey_version(self.chocolateylink())
        if a != b:
            return Version(True, a)
        return Version(False, None)