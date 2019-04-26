import collections
import re
import win32api
import product_utils as productutils
from abc import ABCMeta, abstractmethod
from os import path, getcwd
from urllib import urlretrieve
from urllib2 import urlopen

import win32con


class AbstractPackage(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.temp_path = None
        self.chocolatey_url_pattern = r"https:\/\/chocolatey\.org\/api\/\w\d\/package\/.*"
        self.Version = collections.namedtuple('Version', ['isNew', 'number'])

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

    def version(self, url):
        """ version of file with given url """
        version = None
        if re.match(self.chocolatey_url_pattern, url):
            # reading version out of filename
            split_url = urlopen(url).geturl().split("/")
            filename = split_url[len(split_url) - 1]
            version = filename.split(".")[1:-1]
        else:
            # reading version out of windows-version-info
            version_string = "ProductVersion"
            file_info_language = "\\VarFileInfo\\Translation"
            file_info_string = "\\StringFileInfo\\%04X%04X\\%s"
            response = urlretrieve(url, urlopen(url).geturl().split("/")[-1])
            self.temp_path = path.join(getcwd(), response[0])

            if self.temp_path.endswith("msi"):
                version = productutils.GetMsiProperty(self.temp_path, version_string)
            else:
                languages = win32api.GetFileVersionInfo(self.temp_path, file_info_language)
                for language, codepage in languages:
                    version = win32api.GetFileVersionInfo(self.temp_path,
                                                          file_info_string % (language, codepage, version_string))
            version = version.split(".")
        return version

    def compare(self):
        """ compares versions of two files with given urls """
        a = self.version(self.downloadlink())
        b = self.version(self.chocolateylink())
        different_numbers = [d for d, c in map(None, a, b) if d != c]
        if len(different_numbers) > 0:
            return self.Version(True, a)
        return self.Version(False, b)
