from xml.etree import ElementTree

from packages.package import Package


class Parser(object):
    def __init__(self):
        self.keys = ["name", "type", "links"]
        self.link_keys = ["extern", "chocolatey"]

    def parse(self, xml):
        # das muss schöne gehen -> rekursiv
        package = Package()
        root = ElementTree.parse(xml).getroot()
        for k in self.keys:
            element = next(root.iterfind(k), None)
            if element is not None:
                if len(element) > 1:
                    for link_key in self.link_keys:
                        link = next(element.iterfind(link_key), None)
                        setattr(package, link_key, link.text)
                else:
                    setattr(package, k, element.text)
            elif len(root.attrib) > 0:
                setattr(package, k, root.attrib[k])
        return package
