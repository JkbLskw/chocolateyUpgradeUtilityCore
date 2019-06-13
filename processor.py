import re
import xml.etree.ElementTree as element_tree
import helper.package_helper as helper

from chocolatey import Chocolatey
from packages.deezer import Deezer
from packages.elster import Elster
from packages.cocuun import Cocuun


class Processor(object):

    def __init__(self, chocolatey, packages):
        """ processor for package updates """
        self.chocolatey = chocolatey
        self.packages = packages
        self.chocolatey_checksum_pattern = r"\s+checksum\s+=\s+\'[a-zA-Z0-9]{64}\'"
        self.chocolatey_namespace = "http://schemas.microsoft.com/packaging/2015/06/nuspec.xsd"
        self.chocolatey_xsd = "{" + self.chocolatey_namespace + "}"
        self.version_key = "version"
        self.dot = "."
        self.temp_path = None
        element_tree.register_namespace('', self.chocolatey_namespace)

    def start_flow(self):
        """ starts comparison and file updates of packages """
        for package in self.packages:
            version = package.compare()
            if version.isNew:
                joined_version = self.join_version(version, self.dot)
                changed_nuspec = self.replace_value_xml(package.nuspec(), self.chocolatey_xsd + self.version_key,
                                                        joined_version)
                changed_installscript = self.replace_value_plaintext(package.installscript(),
                                                                     helper.checksum(package.temp_path),
                                                                     self.chocolatey_checksum_pattern)
                if changed_nuspec and changed_installscript:
                    is_packed = self.chocolatey.pack(package.nuspec(), package.packagepath(), joined_version)
                print("[" + type(package).__name__ + "] updated to: "
                      + self.join_version(version, self.dot)
                      + " [nuspec: " + str(changed_nuspec) + "]"
                      + " [installscript: " + str(changed_installscript) + "]"
                      + " [packed: " + str(is_packed) + "]")
            else:
                print("[" + type(package).__name__ + "] up to date")
            package.cleanup()

    def replace_value_xml(self, xml_path, key, value):
        """ find a value with key in xml and replace """
        replaced = False
        tree = element_tree.parse(xml_path)
        for version_element in tree.iter(key):
            version_element.text = value
            replaced = True
        tree.write(xml_path)
        return replaced

    def replace_value_plaintext(self, text_path, value, line_pattern):
        """ find a value with pattern in textfile and replace """
        replaced = False
        content = []
        with open(text_path, 'r') as infile:
            for line in infile.readlines():
                if re.match(line_pattern, line):
                    content.append(line.replace(line.split('\'')[1], value))
                    replaced = True
                else:
                    content.append(line)
        with open(text_path, 'w') as outfile:
            for line in content:
                outfile.write(line)
        return replaced

    def join_version(self, version, delimiter):
        return delimiter.join([str(x) for x in version.number])


if __name__ == "__main__":
    processor = Processor(Chocolatey(), [Cocuun(), Deezer(), Elster()])
    processor.start_flow()
