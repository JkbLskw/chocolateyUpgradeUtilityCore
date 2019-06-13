from abc import ABCMeta, abstractmethod


class AbstractExecutable(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.fileinfo_versionstring = "ProductVersion"

    @abstractmethod
    def version(self, path):
        """ version of package from given url """
        return
