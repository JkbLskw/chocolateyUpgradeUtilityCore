import hashlib


class PackageHelper(object):
    """ helper-class for chocolatey-packages """

    def __init__(self):
        pass

    def checksum(path, hashtype=hashlib.sha256):
        """ checksum of file with given path and hashtype """
        hash256 = hashtype()
        with open(path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                hash256.update(byte_block)
        return hash256.hexdigest()
