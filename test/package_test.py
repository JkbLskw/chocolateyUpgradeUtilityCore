import hashlib
import re
import unittest
from os import path, getcwd
from pathlib import Path

from helper.package_helper import PackageHelper
from packages.deezer import Deezer
from packages.elster import Elster
from packages.jameica import Jameica


class PackageTest(unittest.TestCase):

    def testMsi(self):
        # given
        msiTest = Elster()
        msiTest.download_link = Path(getcwd() + "\\resources\\test.msi").as_uri()
        msiTest.temp_path = PackageHelper.download(msiTest.downloadlink(), msiTest.temp_path)

        # when
        version = msiTest.version(msiTest.temp_path)

        # then
        self.assertListEqual(version, [1, 2, 3, 4])

        # cleanup
        PackageHelper.cleanup(msiTest.temp_path, msiTest.temp_dir)

    def testExe(self):
        # given
        exeTest = Deezer()
        exeTest.download_link = Path(getcwd() + "\\resources\\test.exe").as_uri()

        # when
        exeTest.temp_path = PackageHelper.download(exeTest.downloadlink(), exeTest.temp_path)
        version = exeTest.version(exeTest.temp_path)

        # then
        self.assertListEqual(version, [1, 2, 3, 4])

        # cleanup
        PackageHelper.cleanup(exeTest.temp_path, exeTest.temp_dir)

    def testPlain(self):
        # given
        plainTest = Jameica()
        plainTest.download_link_start = Path(getcwd()).as_uri() + "/resources/"
        plainTest.downloadsite_link = Path(getcwd() + "\\resources\\test.html").as_uri()
        plainTest.download_link_pattern = re.compile("^test-([0-9]|\.)*\.zip$")

        # when
        plainTest.temp_path = PackageHelper.download(plainTest.downloadlink(), plainTest.temp_path)
        version = plainTest.version(plainTest.temp_path)

        # then
        self.assertListEqual(version, [1, 2, 3, 4])

        # cleanup
        PackageHelper.cleanup(plainTest.temp_path, plainTest.temp_dir)

    def testChecksum(self):
        # given
        test_exe_path = getcwd() + "/resources/test.exe"
        test_msi_path = getcwd() + "/resources/test.msi"
        test_zip_path = getcwd() + "/resources/test.zip"

        # hashed exe
        self.assertEqual(PackageHelper.checksum(test_exe_path),
                         "d06c1f80180e0029e604cfd71f1f06ba231be732c4720168dad4be92805cf085")
        self.assertEqual(PackageHelper.checksum(test_exe_path, hashlib.sha1),
                         "a5414b722af8bb1a7356546f13e70e492787c82d")
        self.assertEqual(PackageHelper.checksum(test_exe_path, hashlib.md5),
                         "7e59ed16b2c2cf633357558498a3d6f4")

        # hashed msi
        self.assertEqual(PackageHelper.checksum(test_msi_path),
                         "cb86f952749cc5932538f5051be39b835d32c3e0978b3b79cc585c5b5cc54330")
        self.assertEqual(PackageHelper.checksum(test_msi_path, hashlib.sha1),
                         "fe81ee977c645b28155f11c08f58b6cea24767e4")
        self.assertEqual(PackageHelper.checksum(test_msi_path, hashlib.md5),
                         "5344535916a54f1f16fbd81b585c5a3d")

        # hashed zip
        self.assertEqual(PackageHelper.checksum(test_zip_path),
                         "2b5a6d2b9693b43292b1a442e2d257b0c55551c0276acc297bee750db4655e69")
        self.assertEqual(PackageHelper.checksum(test_zip_path, hashlib.sha1),
                         "7a0a2815e0c4bbb2443d1ac8c29240192ada01c3")
        self.assertEqual(PackageHelper.checksum(test_zip_path, hashlib.md5),
                         "b5dcb1f8edaa5f70c6fa2478e66107e2")