import struct
import tempfile
import unittest
from pathlib import Path

from npkpy.npk.npk import Npk
from npkpy.npk.pckHeader import PckHeader
from tests.constants import DummyHeaderCnt, MAGICBYTES, getDummyNpkBinary


class Test_npkClass(unittest.TestCase):

    def setUp(self) -> None:
        self.npkFile = Path(tempfile.NamedTemporaryFile(suffix=".npk").name)
        self.npkFile.write_bytes(getDummyNpkBinary())

    def test_fileIsNoNpkFile(self):
        self.npkFile.write_bytes(b"NoMagicBytesAtHeadOfFile")

        with self.assertRaises(RuntimeError) as e:
            _ = Npk(self.npkFile).pck_magicBytes
        self.assertEqual(e.exception.args[0], "MagicBytes not found in Npk file")

    def test_npkFileIsCorrupt_fileCorruptException(self):
        self.npkFile.write_bytes(MAGICBYTES + b"CorruptFile")

        with self.assertRaises(RuntimeError) as e:
            _ = Npk(self.npkFile).pck_cntList
        self.assertEqual(e.exception.args[0],
                         f"File maybe corrupted. Please download again. File: {self.npkFile.absolute()}")

    def test_extractMagicBytes(self):
        self.assertEqual(MAGICBYTES, Npk(self.npkFile).pck_magicBytes)

    def test_extractLenOfNpkPayload_propagatedSizeIsValid(self):
        self.assertEqual(len(DummyHeaderCnt().binHeaderCntA), Npk(self.npkFile).pck_payloadLen)

    def test_calculatePckFullSize_equalsFileSize(self):
        self.assertEqual(self.npkFile.stat().st_size, Npk(self.npkFile).pck_fullSize)

    def test_getNpkBinary_equalsOriginalBinary(self):
        npkBinary = self.npkFile.read_bytes()

        self.assertEqual(npkBinary, Npk(self.npkFile).pck_fullBinary)

    def test_getEnumeratedListOfCntInNpk(self):
        cntList = list(Npk(self.npkFile).pck_enumerateCnt)
        cntId, cnt = cntList[0]

        self.assertEqual(1, len(cntList))
        self.assertEqual(0, cntId)
        self.assertTrue(isinstance(cnt, PckHeader))

    def test_getAllCnt_returnAsList(self):
        cntList = Npk(self.npkFile).pck_cntList

        self.assertEqual(1, len(cntList))
        self.assertTrue(isinstance(cntList[0], PckHeader))

    def test_getAllCnt_exceptionWithUnknownCntInNpk(self):
        unknownCnt = DummyHeaderCnt()
        unknownCnt._00_cnt_id = struct.pack("H", 999)
        self.npkFile.write_bytes(getDummyNpkBinary(payload=unknownCnt.binHeaderCntA))

        with self.assertRaises(RuntimeError) as e:
            _ = Npk(self.npkFile).pck_cntList
        self.assertEqual(e.exception.args[0], f"failed with id: 999\n"
                                              f"New cnt id discovered in file: {self.npkFile.absolute()}")


