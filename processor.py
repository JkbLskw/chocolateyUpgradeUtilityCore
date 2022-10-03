from helper.package_helper import PackageHelper
from helper.manipulator import Manipulator
from core.chocolatey import Chocolatey
from helper.parser import Parser
from packages.deezer import Deezer
from packages.elster import Elster
from packages.cocuun import Cocuun
from packages.jameica import Jameica
import logging
import sys

from packages.rocksndiamonds import RocksnDiamonds

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
named_packages = {"deezer":Deezer, "elster":Elster, "cocuun":Cocuun, "jameica":Jameica, "rocksdiamonds":RocksnDiamonds }

class Processor(object):

    @classmethod
    def upgrade(cls, chocolatey, manipulate, packages):
        """ starts comparison and upgrades of packages """
        checksum_pattern = r"\s+checksum\s+=\s+\'[a-zA-Z0-9]{64}\'"
        installation_link_pattern = r"\s+url\s+=\s+\'[a-zA-Z0-9\/\.\:]+\'"
        version_pattern = "version"
        for package in packages:
            logging.info("[%s] comparing versions...", type(package).__name__)
            version = package.compare()
            if version.is_new():
                changed_nuspec = False
                changed_checksum = False
                changed_installation_link = False
                is_packed = False
                if manipulate == "true":
                    manipulator = Manipulator()
                    changed_nuspec = manipulator.xml(package.nuspec(),
                                                     version_pattern,
                                                     version.get())
                    changed_checksum = manipulator.plaintext(package.installscript(),
                                                                  PackageHelper.checksum(package.checksumpath()),
                                                                  checksum_pattern)
                    if package.installationlink() != None:
                        trimmed_version = version.get().split('.')
                        trimmed_version.pop()
                        changed_installation_link = manipulator.plaintext(package.installscript(),
                            package.installationlink() + '.'.join(trimmed_version),
                            installation_link_pattern)
                    is_packed = chocolatey.pack(package.nuspec(), package.packagepath())
                logging.info("[%s] update available from (%s) to (%s) [nuspec: %s][new checksum: %s][new link: %s][packed: %s]",
                             type(package).__name__,
                             version.get(last=True),
                             version.get(),
                             str(changed_nuspec),
                             str(changed_checksum),
                             str(changed_installation_link),
                             is_packed)
            else:
                logging.info("[%s] up to date (%s)", type(package).__name__, version.get(last=True))
            PackageHelper.cleanup(package.temp_path, package.temp_dir)


if __name__ == "__main__":
    # package = Parser().parse("packages/deezer.xml")
    instantiated_packages = []
    base_path = sys.argv[1]
    manipulate = sys.argv[2]
    for arg in sys.argv[3:]:
        instantiated_packages.append(named_packages[arg](base_path))
    Processor.upgrade(Chocolatey(), manipulate, instantiated_packages)

