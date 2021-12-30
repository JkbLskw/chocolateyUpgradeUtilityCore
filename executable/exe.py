import subprocess

from executable.abstract_executable import AbstractExecutable


class Exe(AbstractExecutable):
    """ exe executable """

    def __init__(self):
        AbstractExecutable.__init__(self)
        self.fileinfo_language = "\\VarFileInfo\\Translation"
        self.fileinfo_string = "\\StringFileInfo\\%04X%04X\\%s"

    def version(self, path):
        subprocess.call(r'"7z" x ' + path + ' -o' + ".\\temp\\zip\\1", stdout=subprocess.PIPE)
        subprocess.call(r'"7z" x ' + ".\\temp\\zip\\1\\$PLUGINSDIR\\app-32.7z" + ' -o' + ".\\temp\\zip\\2", stdout=subprocess.PIPE)
        subprocess.call(r'"7z" x ' + ".\\temp\\zip\\2\\Deezer.exe" + ' -o' + ".\\temp\\zip\\3", stdout=subprocess.PIPE)

        with open(".\\temp\\zip\\3\\.rsrc\\1033\\version.txt", 'r') as f:
            for line in f.readlines():
                raw_line = line.replace('\x00', '')
                if 'FILEVERSION' in raw_line:
                    split_line = raw_line.split(' ')
                    version = split_line[len(split_line) - 1].rstrip('\n').replace('\x00', '')
                    break
        return [int(x) for x in version.split(",")]
