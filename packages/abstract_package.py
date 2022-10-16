import re
import sys
from abc import ABCMeta, abstractmethod
from os import getcwd
from urllib.request import urlopen
from packages.version import Version
from helper.package_helper import PackageHelper
import datetime

class AbstractPackage(object):
    __metaclass__ = ABCMeta

    def __init__(self, base_path):
        self.ONE_HUNDRET = 100
        self.MB_BASE2 = 1048576
        self.temp_dir = getcwd() + "\\temp\\"
        self.temp_path = self.temp_dir
        self.chocolatey_url_pattern = r"https:\/\/chocolatey\.org\/api\/\w\d\/package\/.*"
        self.base_package_path = base_path

    @abstractmethod
    def downloadlink(self):
        """download-link of package"""
        return

    @abstractmethod
    def installationlink(self):
        """installation-link of package with specific version"""
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

    @abstractmethod
    def checksumpath(self):
        """filepath for checksum of package"""
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
        current = count_size / self.MB_BASE2
        total = total_size / self.MB_BASE2
        percent = int(count_size * 100 / total_size)
        date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        pattern = "\r%s [%s] downloading... %d%% - %.2f MB of %.2f MB"
        sys.stdout.write(pattern % (date, type(self).__name__, percent, current, total))
        if percent is self.ONE_HUNDRET:
            sys.stdout.write("\r\n")
        sys.stdout.flush()

    def compare(self):
        """ compares versions of two files with given urls """
        chocolatey_version = self.chocolatey_version(self.chocolateylink())
        download_link = self.downloadlink()
        if download_link is None:
            return Version(None, chocolatey_version)
        self.temp_path = PackageHelper.download(download_link, self.temp_path, self.progress)
        download_version = self.version(self.temp_path)
        return Version(download_version, chocolatey_version)