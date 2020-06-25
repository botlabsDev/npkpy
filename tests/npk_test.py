import struct
import tempfile
import unittest
from pathlib import Path

from npkpy.common import NPKError, NPKIdError, NPKMagicBytesError
from npkpy.npk.npk import Npk
from npkpy.npk.pck_header import PckHeader
from tests.constants import DummyHeaderCnt, MAGIC_BYTES, get_dummy_npk_binary


class Test_npkClass(unittest.TestCase):

    def setUp(self) -> None:
        self.npkFile = Path(tempfile.NamedTemporaryFile(suffix=".npk").name)
        self.npkFile.write_bytes(get_dummy_npk_binary())

    def test_fileIsNoNpkFile(self):
        self.npkFile.write_bytes(b"NoMagicBytesAtHeadOfFile")

        with self.assertRaises(NPKMagicBytesError) as e:
            _ = Npk(self.npkFile).pck_magic_bytes
        self.assertEqual(e.exception.args[0], "Magic bytes not found in Npk file")

    def test_npkFileIsCorrupt_fileCorruptException(self):
        self.npkFile.write_bytes(MAGIC_BYTES + b"CorruptFile")

        with self.assertRaises(NPKError) as e:
            _ = Npk(self.npkFile).pck_cnt_list
        self.assertEqual(e.exception.args[0],
                         f"File maybe corrupted. Please download again. File: {self.npkFile.absolute()}")

    def test_extractMagicBytes(self):
        self.assertEqual(MAGIC_BYTES, Npk(self.npkFile).pck_magic_bytes)

    def test_extractLenOfNpkPayload_propagatedSizeIsValid(self):
        self.assertEqual(len(DummyHeaderCnt().get_binary), Npk(self.npkFile).pck_payload_len)

    def test_calculatePckFullSize_equalsFileSize(self):
        self.assertEqual(self.npkFile.stat().st_size, Npk(self.npkFile).pck_full_size)

    def test_getNpkBinary_equalsOriginalBinary(self):
        npkBinary = self.npkFile.read_bytes()

        self.assertEqual(npkBinary, Npk(self.npkFile).pck_full_binary)

    def test_getEnumeratedListOfCntInNpk(self):
        cntList = list(Npk(self.npkFile).pck_enumerate_cnt)
        cntId, cnt = cntList[0]

        self.assertEqual(1, len(cntList))
        self.assertEqual(0, cntId)
        self.assertTrue(isinstance(cnt, PckHeader))

    def test_getAllCnt_returnAsList(self):
        cntList = Npk(self.npkFile).pck_cnt_list

        self.assertEqual(1, len(cntList))
        self.assertTrue(isinstance(cntList[0], PckHeader))

    def test_getAllCnt_exceptionWithUnknownCntInNpk(self):
        unknownCnt = DummyHeaderCnt()
        unknownCnt._00_cnt_id = struct.pack("H", 999)
        self.npkFile.write_bytes(get_dummy_npk_binary(cnt=unknownCnt.get_binary))

        with self.assertRaises(NPKIdError) as e:
            _ = Npk(self.npkFile).pck_cnt_list
        self.assertEqual(e.exception.args[0], f"Failed with cnt id: 999\n"
                                              f"New cnt id discovered in file: {self.npkFile.absolute()}")
