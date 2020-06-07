import tempfile
import unittest
from pathlib import Path

from npkpy.common import getPktInfo, getCntInfo, getAllNkpFiles
from npkpy.npk.npk import Npk


class Common_Test(unittest.TestCase):

    def setUp(self) -> None:
        self.npkFile = Path(tempfile.NamedTemporaryFile(suffix=".npk").name)
        self.npkFile.write_bytes(Path("tests/testData/gps-6.45.6.npk").read_bytes())
        self.npk = Npk(self.npkFile)

    def tearDown(self) -> None:
        if self.npkFile.exists():
            self.npkFile.unlink()

    def test_getBasicPktInfo(self):
        self.assertEqual([(str(self.npkFile.name))], getPktInfo(self.npk))

    def test_getBasicCntInfo(self):
        self.assertEqual(['Cnt:  0:PckHeader',
                          'Cnt:  1:PckReleaseTyp',
                          'Cnt:  2:CntArchitectureTag',
                          'Cnt:  3:PckDescription',
                          'Cnt:  4:PckEckcdsaHash',
                          'Cnt:  5:PckRequirementsHeader',
                          'Cnt:  6:CntNullBlock',
                          'Cnt:  7:CntSquashFsImage',
                          'Cnt:  8:CntSquashFsHashSignature',
                          'Cnt:  9:CntArchitectureTag'], getCntInfo(self.npk), )

    def test_getFullPktInfo(self):
        pass

    #     result = getFullPktInfo(self.npk)
    #
    #     self.assertEqual(['Cnt:  0:PckHeader',
    #                       'Cnt:  1:PckReleaseTyp',
    #                       'Cnt:  2:PckArchitectureTag',
    #                       'Cnt:  3:PckDescription',
    #                       'Cnt:  4:PckSha1Hash',
    #                       'Cnt:  5:PckRequirementsHeader',
    #                       'Cnt:  6:PckNullBlock',
    #                       'Cnt:  7:PckSquashFsImage',
    #                       'Cnt:  8:PckSquashFsHashSignature',
    #                       'Cnt:  9:PckArchitectureTag'], result)

    def test_getFullCntInfo(self):
        pass


class Test_findNpkFiles(unittest.TestCase):

    def setUp(self) -> None:
        self.tmpPath = Path(tempfile.TemporaryDirectory().name)
        self.tmpPath.mkdir(parents=True)
        self.expectedFiles = []

    def tearDown(self) -> None:
        for file in self.tmpPath.rglob("*"):
            if file.is_file():
                file.unlink()
        for folder in sorted(self.tmpPath.rglob("*"), key=lambda _path: str(_path.absolute()).count("/"), reverse=True):
            folder.rmdir()
        self.tmpPath.rmdir()

    def test_findMultipleNpkFiles_inFolder(self):
        self.addExistingFiles(["fileA.npk", "fileB.npk", "fileC.npk"])

        self.assertExistingFiles(sorted(getAllNkpFiles(self.tmpPath)))

    def test_findMultipleNpkFilesRecursive(self):
        self.addExistingFiles(["fileA.npk", "subB/fileB.npk", "subB/subC/fileC.npk"])

        self.assertExistingFiles(sorted(getAllNkpFiles(self.tmpPath)))

    def test_selectOnlyNpkFiles(self):
        self.addExistingFiles(["fileA.npk", "fileB.exe", "fileC.txt"])

        self.expectedFiles = [self.tmpPath / "fileA.npk"]

        self.assertExistingFiles(sorted(getAllNkpFiles(self.tmpPath)))

    def test_globOnlyNpkFilesFittingPattern(self):
        self.addExistingFiles(["fi__pattern__leA.npk", "fileB.npk", "fi__pattern__leC.exe", "fileD.exe"])

        self.expectedFiles = [self.tmpPath / "fi__pattern__leA.npk"]

        self.assertExistingFiles(sorted(getAllNkpFiles(self.tmpPath, containStr="__pattern__")))

    def assertExistingFiles(self, result):
        self.assertEqual(self.expectedFiles, result)

    def addExistingFiles(self, files):
        for file in files:
            f = self.tmpPath / file
            f.parent.mkdir(parents=True, exist_ok=True)
            f.touch()
            self.expectedFiles.append(f)
