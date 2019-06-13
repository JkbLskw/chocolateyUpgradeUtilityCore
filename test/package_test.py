import unittest
from os import path, getcwd
from pathlib import Path

from packages.deezer import Deezer
from packages.elster import Elster


class PackageTest(unittest.TestCase):

    def testMsi(self):
        msiTest = Elster()
        msiTest.download_link = Path(getcwd() + "\\resources\\test.msi").as_uri()
        version = msiTest.version(msiTest.download(msiTest.downloadlink()))
        self.assertListEqual(version, [1, 2, 3, 4])

    def testExe(self):
        exeTest = Deezer()
        exeTest.download_link = Path(getcwd() + "\\resources\\test.exe").as_uri()
        version = exeTest.version(exeTest.download(exeTest.downloadlink()))
        self.assertListEqual(version, [1, 2, 3, 4])
