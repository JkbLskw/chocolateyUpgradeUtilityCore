from execuable.exe import Exe
from packages.abstract_package import AbstractPackage


class Deezer(AbstractPackage, Exe):
    """ deezer package """

    def __init__(self):
        Exe.__init__(self)
        AbstractPackage.__init__(self)
        self.chocolatey_link = "https://chocolatey.org/api/v2/package/deezer"
        self.package_path = "D:/Chocolatey_Packages/deezer-package/"
        self.package_tools_path = "tools/"
        self.nuspec_name = "deezer.nuspec"
        self.install_script_name = "chocolateyInstall.ps1"
        self.uninstall_script_name = "chocolateyUninstall.ps1"
        self.download_link = "https://www.deezer.com/desktop/download?platform=win32&architecture=x86"

    def downloadlink(self):
        return self.download_link

    def chocolateylink(self):
        return self.chocolatey_link

    def packagepath(self):
        return self.package_path

    def nuspec(self):
        return self.packagepath() + self.nuspec_name

    def installscript(self):
        return self.packagepath() + self.package_tools_path + self.install_script_name

    def uninstallscript(self):
        return self.packagepath() + self.package_tools_path + self.uninstall_script_name
