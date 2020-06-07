import unittest
from pathlib import Path
from tempfile import NamedTemporaryFile

from tools.sections import findDiffs


class FindDiffs_Test(unittest.TestCase):
    def setUp(self) -> None:
        self.fileA = Path(NamedTemporaryFile(delete=False).name)
        self.fileB = Path(NamedTemporaryFile(delete=False).name)
        self.fileC = Path(NamedTemporaryFile(delete=False).name)

    def tearDown(self) -> None:
        self.fileA.unlink()
        self.fileB.unlink()
        self.fileC.unlink()

    def test_filesEqual_minimumFile(self):
        self.assertFileDiff("a", "a", [(0, 0, False)])

    def test_filesUnequal_minimumFile(self):
        self.assertFileDiff("a", "b", [(0, 0, True)])

    def test_filesEqual_equalSize(self):
        self.assertFileDiff("aabbcc", "aabbcc", [(0, 5, False)])

    def test_diffInCenter_equalSize(self):
        self.assertFileDiff("aabbcc", "aa  cc", [(0, 1, False), (2, 3, True), (4, 5, False)])

    def test_differInSize(self):
        self.assertFileDiff("aa", "aabb", [(0, 1, False)])

    def assertFileDiff(self, contentA, contentB, result):
        writeFile(self.fileA, contentA)
        writeFile(self.fileB, contentB)

        self.assertEqual(result, findDiffs(self.fileA, self.fileB))


def writeFile(file, content):
    with file.open("w") as f:
        f.write(content)
