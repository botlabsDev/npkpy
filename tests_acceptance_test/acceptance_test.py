import subprocess
import tempfile
import unittest
from pathlib import Path


class Test_npkpy(unittest.TestCase):

    def setUp(self) -> None:
        # TODO: create DummyPkg and replace gps-6.45.6.npk
        self.npk_file = Path("tests/testData/gps-6.45.6.npk")
        self.path_to_npk = str(self.npk_file.absolute())
        self.npk_container_list = Path("tests/testData/gps-6.45.6.result").read_text()
        self.dst_folder = Path(tempfile.mkdtemp())

    def tearDown(self) -> None:
        for _file in self.dst_folder.rglob("*"):
            if _file.is_file():
                _file.unlink()
        for _file in self.dst_folder.rglob("*"):
            _file.rmdir()

        self.dst_folder.rmdir()

    def test_list_all_containers_from_npk_pkg(self):
        cmd = ["npkpy", "--file", self.path_to_npk, "--show-container"]
        output = run_command_in_terminal(cmd)
        self.assertEqual(self.npk_container_list, output)

    def test_list_in_folder(self):
        cmd = ["npkpy", "--src-folder", str(self.npk_file.parent), "--show-container"]
        output = run_command_in_terminal(cmd)
        self.assertEqual(self.npk_container_list, output)

    def test_export_all_container_from_npk(self):
        cmd = ["npkpy", "--file", self.path_to_npk, "--dst-folder", self.dst_folder.absolute(), "--export-all"]

        run_command_in_terminal(cmd)

        exported_container = sorted(str(_file.relative_to(self.dst_folder)) for _file in self.dst_folder.rglob('*'))
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
                          'npkPyExport_gps-6.45.6/009_cnt_CntArchitectureTag.raw'], exported_container)

    def test_extract_squashfs_container_from_npk(self):
        cmd = ["npkpy", "--file", self.path_to_npk, "--dst-folder", self.dst_folder.absolute(), "--export-squashfs"]

        run_command_in_terminal(cmd)

        self.assert_container_extracted(['npkPyExport_gps-6.45.6',
                                         'npkPyExport_gps-6.45.6/007_cnt_CntSquashFsImage.raw'])

    def test_extract_zlib_container_from_npk_nonexisting_not_extracted(self):
        cmd = ["npkpy", "--file", self.path_to_npk, "--dst-folder", self.dst_folder.absolute(), "--export-zlib"]

        run_command_in_terminal(cmd)

        self.assert_container_extracted([])

    def assert_container_extracted(self, expected_files):
        extracted_container = sorted(str(_file.relative_to(self.dst_folder)) for _file in self.dst_folder.rglob('*'))
        self.assertEqual(expected_files, extracted_container)


def run_command_in_terminal(cmd):
    return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True).stdout.decode("UTF-8")
