import abc
from abstract_package import AbstractPackage


class Deezer(AbstractPackage):
    """ deezer package """

    def downloadlink(self):
        # test
        # return "file:///C:/Users/gj2SprpWCV/Downloads/DeezerDesktopSetup_4.5.1.exe"
        return "https://www.deezer.com/desktop/download?platform=win32&architecture=x86"

    def chocolateylink(self):
        return "https://chocolatey.org/api/v2/package/deezer"

    def packagepath(self):
        return "D:/Chocolatey_Packages/deezer-package/"

    def nuspec(self):
        return self.packagepath() + "deezer.nuspec"

    def installscript(self):
        return self.packagepath() + "tools/chocolateyInstall.ps1"

    def uninstallscript(self):
        return self.packagepath() + "tools/chocolateyUninstall.ps1"
