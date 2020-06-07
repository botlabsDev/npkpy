import subprocess
import tempfile
import unittest
from pathlib import Path


class Test_npkPy(unittest.TestCase):

    def setUp(self) -> None:
        # TODO: create DummyPkg and replace gps-6.45.6.npk
        self.npkFile = Path("tests/testData/gps-6.45.6.npk")
        self.pathToNpk = str(self.npkFile.absolute())
        self.npkContainerList = Path("tests/testData/gps-6.45.6.result").read_text()
        self.dstFolder = Path(tempfile.mkdtemp())

    def tearDown(self) -> None:
        [f.unlink() for f in self.dstFolder.rglob("*") if f.is_file()]
        [f.rmdir() for f in self.dstFolder.rglob("*")]
        self.dstFolder.rmdir()

    def test_showAllContainersFromNpkPkg(self):
        cmd = ["npkPy", "--file", self.pathToNpk, "--showContainer"]
        output = runCmdInTerminal(cmd)
        self.assertEqual(self.npkContainerList, output)

    def test_exportAllContainerFromNpk(self):
        cmd = ["npkPy", "--file", self.pathToNpk, "--dstFolder", self.dstFolder.absolute(), "--exportAll"]

        runCmdInTerminal(cmd)

        exportedContainer = sorted(str(f.relative_to(self.dstFolder)) for f in self.dstFolder.rglob('*'))
        self.assertEqual(['npkPyExport_gps-6.45.6',
                          'npkPyExport_gps-6.45.6/000_cnt_PckHeader.raw',
                          'npkPyExport_gps-6.45.6/001_cnt_PckReleaseTyp.raw',
                          'npkPyExport_gps-6.45.6/002_cnt_CntArchitectureTag.raw',
                          'npkPyExport_gps-6.45.6/003_cnt_PckDescription.raw',
                          'npkPyExport_gps-6.45.6/004_cnt_PckEckcdsaHash.raw',
                          'npkPyExport_gps-6.45.6/005_cnt_PckRequirementsHeader.raw',
                          'npkPyExport_gps-6.45.6/006_cnt_CntNullBlock.raw',
                          'npkPyExport_gps-6.45.6/007_cnt_CntSquashFsImage.raw',
                          'npkPyExport_gps-6.45.6/008_cnt_CntSquashFsHashSignature.raw',
                          'npkPyExport_gps-6.45.6/009_cnt_CntArchitectureTag.raw'], exportedContainer)

    def test_extractSquashFsContainerFromNpk(self):
        cmd = ["npkPy", "--file", self.pathToNpk, "--dstFolder", self.dstFolder.absolute(), "--exportSquashFs"]

        runCmdInTerminal(cmd)

        self.assertContainerExtracted(['npkPyExport_gps-6.45.6',
                                       'npkPyExport_gps-6.45.6/007_cnt_CntSquashFsImage.raw'])

    #
    def test_extractZlibContainerFromNpk_NonExisitngNotExtracted(self):
        cmd = ["npkPy", "--file", self.pathToNpk, "--dstFolder", self.dstFolder.absolute(), "--exportZlib"]

        runCmdInTerminal(cmd)

        self.assertContainerExtracted([])

    def assertContainerExtracted(self, expectedFiles):
        extractedContainer = sorted(str(f.relative_to(self.dstFolder)) for f in self.dstFolder.rglob('*'))
        self.assertEqual(expectedFiles, extractedContainer)


def runCmdInTerminal(cmd):
    return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.decode("UTF-8")
