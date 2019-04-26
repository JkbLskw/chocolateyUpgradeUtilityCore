import abc
from abstract_package import AbstractPackage


class Elster(AbstractPackage):
    """ elster-formular package """

    def chocolateylink(self):
        return "https://chocolatey.org/api/v2/package/elsterformular"

    def packagepath(self):
        return "D:/Chocolatey_Packages/elsterformular-package/"

    def nuspec(self):
        return self.packagepath() + "elsterformular.nuspec"

    def installscript(self):
        return self.packagepath() + "tools/chocolateyInstall.ps1"

    def uninstallscript(self):
        return self.packagepath() + "tools/chocolateyUninstall.ps1"

    def downloadlink(self):
        return "https://download.elster.de/aktuell/ElsterFormularKomplett.msi"
