import re
import urllib

from bs4 import BeautifulSoup

from executable.plain import Plain
from packages.abstract_package import AbstractPackage


class Jameica(AbstractPackage, Plain):
    """ jameica package """

    def __init__(self):
        Plain.__init__(self)
        AbstractPackage.__init__(self)
        self.chocolatey_link = "https://chocolatey.org/api/v2/package/jameica"
        self.package_path = "D:/Chocolatey_Packages/jameica-package/"
        self.package_tools_path = "tools/"
        self.nuspec_name = "jameica.nuspec"
        self.install_script_name = "chocolateyInstall.ps1"
        self.uninstall_script_name = "chocolateyUninstall.ps1"
        self.download_link_start = "https://www.willuhn.de/products/jameica/"
        self.download_link_pattern = re.compile("^releases\/current\/jameica\/jameica-win64-([0-9]|\.)*\.zip$")
        self.downloadsite_link = "https://www.willuhn.de/products/jameica/download.php"
        self.executable_temp_dir = "jameica"
        self.executable_name = "jameica-win64.exe"

    def downloadlink(self):
        content = urllib.request.urlopen(self.downloadsite_link).read()
        parsed_content = BeautifulSoup(content, 'html.parser')
        download_link_tags = [a for a in parsed_content.find_all('a') if
                re.match(self.download_link_pattern, a.get("href")) is not None]
        download_link = None
        if download_link_tags is not None:
            download_link = self.download_link_start + download_link_tags[0].get("href")
        return download_link

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

    def checksumpath(self):
        return self.temp_path