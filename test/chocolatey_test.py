import unittest
from os import getcwd

from core.chocolatey import Chocolatey


class ChocolateyTest(unittest.TestCase):

    def testChocolateyPack(self):
        resource_path = getcwd() + "\\resources\\testpackage\\"
        nuspec_path = resource_path + "testpackage.nuspec"
        not_nuspec = resource_path + "not.nuspec"
        chocolatey = Chocolatey()
        self.assertTrue(chocolatey.pack(nuspec_path, resource_path))
        self.assertFalse(chocolatey.pack(not_nuspec, resource_path))
