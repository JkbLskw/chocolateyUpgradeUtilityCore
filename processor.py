from helper.package_helper import PackageHelper
from helper.manipulator import Manipulator
from core.chocolatey import Chocolatey
from packages.deezer import Deezer
from packages.elster import Elster
from packages.cocuun import Cocuun
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')


class Processor(object):

    @classmethod
    def upgrade(cls, chocolatey, packages):
        """ starts comparison and upgrades of packages """
        checksum_pattern = r"\s+checksum\s+=\s+\'[a-zA-Z0-9]{64}\'"
        version_pattern = "version"
        for package in packages:
            version = package.compare()
            if version.is_new():
                manipulator = Manipulator()
                changed_nuspec = manipulator.xml(package.nuspec(),
                                                 version_pattern,
                                                 version.get_number())
                changed_installscript = manipulator.plaintext(package.installscript(),
                                                              PackageHelper.checksum(package.temp_path),
                                                              checksum_pattern)
                if changed_nuspec and changed_installscript:
                    is_packed = chocolatey.pack(package.nuspec(), package.packagepath())
                    logging.info("[%s] updated to %s [nuspec: %s][installscript: %s][packed: %s]",
                                 type(package).__name__,
                                 version.get_number(),
                                 str(changed_nuspec),
                                 str(changed_installscript,
                                     str(is_packed)))
            else:
                logging.info("[%s] up to date", type(package).__name__)
            package.cleanup()


if __name__ == "__main__":
    Processor.upgrade(Chocolatey(), [Cocuun()])
