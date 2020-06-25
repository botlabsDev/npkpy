import unittest
from pathlib import Path

from npkpy.npk.npk_file_basic import FileBasic, ARCHITECTURES


class FileInfo_Test(unittest.TestCase):
    def setUp(self) -> None:
        self.file = FileBasic(Path("file-name-1.2.3.npk"))
        self.illegal_file = FileBasic(Path("illegalFIle.abc"))

    def test_file(self):
        self.assertEqual(Path("file-name-1.2.3.npk"), self.file.file)

    def test_versionName(self):
        self.assertEqual("1.2.3", self.file.filename_version)

    def test_versionName_filenameDoesntMatchFormat(self):
        self.assertEqual("<NoVersionMatch>", self.illegal_file.filename_version)

    def test_programName(self):
        self.assertEqual("file-name", self.file.filename_program_name)

    def test_programName_filenameDoesntMatchFormat(self):
        self.assertEqual("<NoProgramNameMatch>", self.illegal_file.filename_program_name)

    def test_programSuffix(self):
        self.assertEqual("npk", self.file.filename_suffix)

    def test_programSuffix_filenameDoesntMatchFormat(self):
        self.assertEqual("<NoSuffixMatch>", self.illegal_file.filename_suffix)

    def test_filenameArchitecture_returnDefaultIfNotMentionedInFilename(self):
        self.assertEqual("x86", self.file.filename_architecture)

    def test_filenameArchitecture_validateArchitectures(self):
        for arch in ARCHITECTURES:
            self.assertEqual(arch, FileBasic(Path(f"file-name-1.2.3-{arch}.npk")).filename_architecture)
