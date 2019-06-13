from packages.abstract_package import AbstractPackage
from execuable.msi import Msi


class Elster(AbstractPackage, Msi):
    """ elster-formular package """

    def __init__(self):
        Msi.__init__(self)
        AbstractPackage.__init__(self)
        self.chocolatey_link = "https://chocolatey.org/api/v2/package/elsterformular"
        self.package_path = "D:/Chocolatey_Packages/elsterformular-package/"
        self.package_tools_path = "tools/"
        self.nuspec_name = "elsterformular.nuspec"
        self.install_script_name = "chocolateyInstall.ps1"
        self.uninstall_script_name = "chocolateyUninstall.ps1"
        self.download_link = "https://download.elster.de/aktuell/ElsterFormularKomplett.msi"

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

    def downloadlink(self):
        return self.download_link
