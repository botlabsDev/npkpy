import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

from npkpy.common import get_short_pkt_info, get_short_cnt_info, get_all_nkp_files, write_to_file, extract_container, \
    get_full_cnt_info, get_full_pkt_info, sha1_sum_from_binary, sha1_sum_from_file
from npkpy.npk.cnt_basic import CntBasic
from npkpy.npk.npk import Npk
from npkpy.npk.pck_header import NPK_PCK_HEADER
from tests.constants import get_dummy_npk_binary, DummyHeaderCnt, get_dummy_basic_cnt


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

        self.assertExistingFiles(sorted(get_all_nkp_files(self.tmpPath)))

    def test_findMultipleNpkFilesRecursive(self):
        self.addExistingFiles(["fileA.npk", "subB/fileB.npk", "subB/subC/fileC.npk"])

        self.assertExistingFiles(sorted(get_all_nkp_files(self.tmpPath)))

    def test_selectOnlyNpkFiles(self):
        self.addExistingFiles(["fileA.npk", "fileB.exe", "fileC.txt"])

        self.expectedFiles = [self.tmpPath / "fileA.npk"]

        self.assertExistingFiles(sorted(get_all_nkp_files(self.tmpPath)))

    def test_globOnlyNpkFilesFittingPattern(self):
        self.addExistingFiles(["fi__pattern__leA.npk", "fileB.npk", "fi__pattern__leC.exe", "fileD.exe"])

        self.expectedFiles = [self.tmpPath / "fi__pattern__leA.npk"]

        self.assertExistingFiles(sorted(get_all_nkp_files(self.tmpPath, contain_str="__pattern__")))

    def assertExistingFiles(self, result):
        self.assertEqual(self.expectedFiles, result)

    def addExistingFiles(self, files):
        for file in files:
            f = self.tmpPath / file
            f.parent.mkdir(parents=True, exist_ok=True)
            f.touch()
            self.expectedFiles.append(f)


class Common_Test(unittest.TestCase):
    def setUp(self) -> None:
        self.payload = "THIS\nIS\nA\nDUMMY\nSTRING\n\n"
        self.file = Path(tempfile.NamedTemporaryFile().name)
        self.file.touch()

        self.output_folder = Path(tempfile.TemporaryDirectory().name)
        self.output_folder.mkdir()

    def tearDown(self) -> None:
        def delete_directory(folder):
            for _file in folder.rglob("*"):
                if _file.is_file():
                    _file.unlink()
                else:
                    delete_directory(_file)
                    _file.rmdir()

        self.file.unlink()
        delete_directory(self.output_folder)

    def test_writeDataToFile_storeOneDataElement(self):
        write_to_file(self.file, self.payload.encode())

        with self.file.open("r") as _file:
            self.assertEqual(self.payload, _file.read())

    def test_writeDataToFile_storeList(self):
        payload_list = [self.payload.encode(), self.payload.encode()]

        write_to_file(self.file, payload_list)

        with self.file.open("r") as _file:
            self.assertEqual(self.payload + self.payload, _file.read())

    def test_getPktInfo_returnOnlyFileName(self):
        npkFile = Mock()
        npkFile.file = self.file

        self.assertEqual([self.file.name], get_short_pkt_info(npkFile))

    def test_getBasicCntInfo(self):
        self.file.write_bytes(get_dummy_npk_binary())

        self.assertEqual(['Cnt:  0:PckHeader'], get_short_cnt_info(Npk(self.file)))

    def test_extractPayloadFromCnt_createFilesWithPayload(self):
        self.file.write_bytes(get_dummy_npk_binary())
        npkFile = Npk(self.file)

        extract_container(npkFile, self.output_folder, [NPK_PCK_HEADER])

        created_files = list(self.output_folder.rglob("*"))

        self.assertEqual(1, len(created_files))

        self.assertEqual([self.output_folder / '000_cnt_PckHeader.raw'], created_files)
        self.assertEqual(DummyHeaderCnt()._02_payload, created_files[0].read_bytes())

    def test_getFullCntInfo_asString(self):
        result = get_full_cnt_info(CntBasic(get_dummy_basic_cnt(), offset_in_pck=0))

        self.assertEqual(['CntBasic',
                          '  Cnt id:           -1',
                          '  Cnt offset:       0',
                          '  Cnt len:          13',
                          '  Payload len:      7',
                          "  Payload[0:7]:    b'Payload' [...] "], result)

    def test_getFullPktInfo_asString(self):
        self.file.write_bytes(get_dummy_npk_binary())
        npkFile = Npk(self.file)

        result = get_full_pkt_info(npkFile)

        self.assertEqual([f"{self.file.name}",
                          'Cnt:  0:PckHeader',
                          'PckHeader',
                          '  Cnt id:           1',
                          '  Cnt offset:       8',
                          '  Cnt len:          41',
                          '  Payload len:      35',
                          "  Payload[0:10]:    b'0123456789' [...] ",
                          '  Program name:     01234567890abcde',
                          '  Os version:       1.2.3 - rc(?): 4',
                          '  Created at:       1970-01-01 00:00:01',
                          '  NullBlock:        (0, 0, 0, 0)',
                          '  Flags:            (0, 0, 0, 0, 0, 0, 0)'], result)

    def test_generateSha1FromFile(self):
        expectedHash = b'\xbb\xbc\xf2\xc5\x943\xf6\x8f"7l\xd2C\x9dl\xd3\t7\x8d\xf6'
        self.file.write_bytes(b"TESTDATA")

        self.assertEqual(expectedHash, sha1_sum_from_file(self.file))

    def test_generateSha1FromHash(self):
        expectedHash = b'\xbb\xbc\xf2\xc5\x943\xf6\x8f"7l\xd2C\x9dl\xd3\t7\x8d\xf6'
        self.assertEqual(expectedHash, sha1_sum_from_binary(b"TESTDATA"))

    def test_generateSha1FromHash_returnEmptyIfNoData(self):
        self.assertEqual(b"<empty>", sha1_sum_from_binary(b""))
