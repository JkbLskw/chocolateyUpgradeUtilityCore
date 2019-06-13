import unittest
from os import getcwd
from pathlib import Path

from chocolatey import Chocolatey


class ChocolateyTest(unittest.TestCase):

    def testChocolateyPack(self):
        resource_path = getcwd() + "\\resources\\testpackage\\"
        nuspec_path = resource_path + "testpackage.nuspec"
        not_nuspec = resource_path + "not.nuspec"
        chocolatey = Chocolatey()
        self.assertTrue(chocolatey.pack(nuspec_path, resource_path, "1.2.3.4"))
        self.assertFalse(chocolatey.pack(not_nuspec, resource_path, "1.2.3.4"))
