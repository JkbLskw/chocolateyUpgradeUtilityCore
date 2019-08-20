import hashlib
from os import path, remove, mkdir, rmdir, listdir
from urllib.request import urlopen, urlretrieve


class PackageHelper(object):
    """ helper-class for chocolatey-packages """

    def checksum(path, hashtype=hashlib.sha256):
        """ checksum of file with given path and hashtype
        :param hashtype: type of hashing
        :return: hex digest of hash
        """
        hash256 = hashtype()
        with open(path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                hash256.update(byte_block)
        return hash256.hexdigest()

    @staticmethod
    def download(url, temp_path, progress_hook=None):
        if not path.exists(temp_path):
            mkdir(temp_path, 755)
        temp_path = temp_path + urlopen(url).geturl().split("/")[-1]
        response = urlretrieve(url, temp_path, progress_hook)
        return temp_path

    @staticmethod
    def cleanup(temp_path, temp_dir):
        if path.exists(temp_path):
            remove(temp_path)
        if path.exists(temp_dir) and len(listdir(temp_dir)) is 0:
            rmdir(temp_dir)
