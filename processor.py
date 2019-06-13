from helper.package_helper import PackageHelper
from helper.manipulator import Manipulator


from core.chocolatey import Chocolatey
from packages.deezer import Deezer
from packages.elster import Elster

# TODO: making CLI out of this
class Processor(object):

    def __init__(self, chocolatey, packages):
        """ processor for package updates """
        self.chocolatey = chocolatey
        self.packages = packages
        self.checksum_pattern = r"\s+checksum\s+=\s+\'[a-zA-Z0-9]{64}\'"
        self.version_pattern = "version"

    def start_flow(self):
        """ starts comparison and file updates of packages """
        for package in self.packages:
            version = package.compare()
            if version.is_new():
                manipulator = Manipulator()
                changed_nuspec = manipulator.xml(package.nuspec(),
                                                 self.version_pattern,
                                                 version.get_number())
                changed_installscript = manipulator.plaintext(package.installscript(),
                                                              PackageHelper.checksum(package.temp_path),
                                                              self.checksum_pattern)
                if changed_nuspec and changed_installscript:
                    is_packed = self.chocolatey.pack(package.nuspec(), package.packagepath())
                print("[" + type(package).__name__ + "] updated to: "
                      + version.get_number()
                      + " [nuspec: " + str(changed_nuspec) + "]"
                      + " [installscript: " + str(changed_installscript) + "]"
                      + " [packed: " + str(is_packed) + "]")
            else:
                print("[" + type(package).__name__ + "] up to date")
            package.cleanup()


if __name__ == "__main__":
    processor = Processor(Chocolatey(), [Deezer(), Elster()])
    processor.start_flow()
