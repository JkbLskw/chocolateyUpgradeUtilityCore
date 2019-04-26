import re
import xml.etree.ElementTree as element_tree
import hashlib

from chocolatey import Chocolatey
from packages.deezer import Deezer
from packages.elster import Elster


class Processor(object):

    def __init__(self, chocolatey, packages):
        """ processor for package updates """
        self.chocolatey = chocolatey
        self.packages = packages
        self.chocolatey_checksum_pattern = r"\s+checksum\s+=\s+\'[a-z0-9]{64}\'"
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
            # version = package.Version(True, ["9", "9", "9"])
            if version.isNew:
                self.replace_value_xml(package.nuspec(), self.chocolatey_xsd + self.version_key,
                                       self.dot.join(version.number))
                self.replace_value_plaintext(package.installscript(), self.checksum(package.temp_path),
                                             self.chocolatey_checksum_pattern)
                is_packed = self.chocolatey.pack(package.nuspec(), package.packagepath())
                print("[" + type(package).__name__ + "] updated to: " + ".".join(version.number))
            else:
                print("[" + type(package).__name__ + "] up to date")

    def replace_value_xml(self, xml_path, key, value):
        """ find a value with key in xml and replace """
        tree = element_tree.parse(xml_path)
        for version_element in tree.iter(key):
            version_element.text = value
        tree.write(xml_path)

    def replace_value_plaintext(self, text_path, value, line_pattern):
        """ find a value with pattern in textfile and replace """
        with open(text_path, 'r') as infile:
            content = [line.replace(line.split('\'')[1], value) if re.match(line_pattern, line) else line for line in
                       infile.readlines()]
        with open(text_path, 'w') as outfile:
            for line in content:
                outfile.write(line)

    def checksum(self, path, hashtype=hashlib.sha256):
        """ checksum of file with given path and hashtype """
        with open(path) as f:
            h = hashtype(f.read())
        return h.hexdigest()


if __name__ == "__main__":
    processor = Processor(Chocolatey(), [Elster(), Deezer()])
    processor.start_flow()
