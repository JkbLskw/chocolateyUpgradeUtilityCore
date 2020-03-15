import win32api

from executable.abstract_executable import AbstractExecutable


class Exe(AbstractExecutable):
    """ exe executable """

    def __init__(self):
        AbstractExecutable.__init__(self)
        self.fileinfo_language = "\\VarFileInfo\\Translation"
        self.fileinfo_string = "\\StringFileInfo\\%04X%04X\\%s"

    def version(self, path):
        languages = win32api.GetFileVersionInfo(path, self.fileinfo_language)
        for language, code in languages:
            fileinfo = self.fileinfo_string % (language, code, self.fileinfo_versionstring)
            # get first version info
            return [int(x) for x in win32api.GetFileVersionInfo(path, fileinfo).split(".")]
