import unittest
from pathlib import Path

from npkpy.npk.npkFileBasic import FileBasic


class FileInfo_Test(unittest.TestCase):
    def setUp(self) -> None:
        self.file = FileBasic(Path("advanced-tools-6.41.3.npk"))

    def test_file(self):
        self.assertEqual(Path("advanced-tools-6.41.3.npk"), self.file.file)

    def test_versionName(self):
        self.assertEqual("6.41.3", self.file.filename_version)

    def test_programName(self):
        self.assertEqual("advanced-tools", self.file.filename_program)

    def test_programSuffix(self):
        self.assertEqual("npk", self.file.filename_suffix)
