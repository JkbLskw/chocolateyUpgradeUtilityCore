import xml.etree.ElementTree as ElementTree
import re


class Manipulator(object):

    def __init__(self):
        self.namespace = "http://schemas.microsoft.com/packaging/2015/06/nuspec.xsd"
        self.xsd = "{" + self.namespace + "}"
        ElementTree.register_namespace('', self.namespace)

    def xml(self, path, key, value):
        """ find a value with key in xml and replace """
        replaced = False
        tree = ElementTree.parse(path)
        for version_element in tree.iter(self.xsd + key):
            version_element.text = value
            replaced = True
        tree.write(path)
        return replaced

    def plaintext(self, path, value, line_pattern):
        """ find a value with pattern in text-file and replace """
        replaced = False
        content = []
        with open(path, 'r') as infile:
            for line in infile.readlines():
                if re.match(line_pattern, line):
                    content.append(line.replace(line.split('\'')[1], value))
                    replaced = True
                else:
                    content.append(line)
        with open(path, 'w') as outfile:
            for line in content:
                outfile.write(line)
        return replaced
