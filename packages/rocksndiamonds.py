from executable.exe import Exe
from packages.abstract_package import AbstractPackage


class RocksnDiamonds(AbstractPackage, Exe):
    """ Rocks'n'Diamonds package """

    def __init__(self, base_path):
        Exe.__init__(self)
        AbstractPackage.__init__(self, base_path)
        self.chocolatey_link = "https://chocolatey.org/api/v2/package/rocksndiamonds"
        self.package_path = "rocksndiamonds-package/"
        self.package_tools_path = "tools/"
        self.nuspec_name = "rocksndiamonds.nuspec"
        self.install_script_name = "chocolateyInstall.ps1"
        self.uninstall_script_name = "chocolateyUninstall.ps1"
        self.download_link = "https://www.artsoft.org/RELEASES/win64/rocksndiamonds/rocksndiamonds-4.2.3.1-win64-setup.exe"

    def downloadlink(self):
        return self.download_link

    def chocolateylink(self):
        return self.chocolatey_link

    def packagepath(self):
        return self.base_package_path + self.package_path

    def nuspec(self):
        return self.packagepath() + self.nuspec_name

    def installscript(self):
        return self.packagepath() + self.package_tools_path + self.install_script_name

    def uninstallscript(self):
        return self.packagepath() + self.package_tools_path + self.uninstall_script_name

    def checksumpath(self):
        return self.temp_path