from execuable.exe import Exe
from packages.abstract_package import AbstractPackage


class Jameica(AbstractPackage, Exe):
    """ jameica package """

    def __init__(self):
        Exe.__init__(self)
        AbstractPackage.__init__(self, zipped=True)
        self.chocolatey_link = "https://chocolatey.org/api/v2/package/jameica"
        self.package_path = "D:/Chocolatey_Packages/jameica-package/"
        self.package_tools_path = "tools/"
        self.nuspec_name = "jameica.nuspec"
        self.install_script_name = "chocolateyInstall.ps1"
        self.uninstall_script_name = "chocolateyUninstall.ps1"
        self.download_link = "https://www.willuhn.de/products/jameica/releases/current/jameica/jameica-win64-2.8.6.zip"
        self.executable_path = "jameica/jameica-win64.exe"

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

    def executablepath(self):
        return self.executable_path
