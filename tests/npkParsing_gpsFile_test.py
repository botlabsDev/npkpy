import datetime
import unittest
from pathlib import Path

from npkpy.npk.npk import Npk, MAGICBYTES


class GpsFile_Test(unittest.TestCase):
    def setUp(self) -> None:
        self.npkFile = Path("tests/testData/gps-6.45.6.npk")
        self.npk = Npk(self.npkFile)
        self.cnt = self.npk.pck_cntList


class ParseGpsNpkFile_Test(GpsFile_Test):

    def test_fileInfos(self):
        self.assertEqual('gps', self.npk.filename_program)
        self.assertEqual('6.45.6', self.npk.filename_version)
        self.assertEqual('npk', self.npk.filename_suffix)
        self.assertEqual('x86', self.npk.filename_architecture)
        self.assertEqual(b'\xc6\x16\xf0\x9d~lS\xa7z\xba}.\xe5\xa6w=\xe9\xb4S\xe7', self.npk.file_hash)

    def test_NpkHeader(self):
        self.assertEqual(MAGICBYTES, self.npk.pck_magicBytes)
        self.assertEqual(53321, self.npk.pck_payloadLen)
        self.assertEqual(53329, self.npk.pck_fullSize)

    def test_PckHeader(self):
        self.assertEqual(1, self.npk.pck_header.cnt_id)
        self.assertEqual("PckHeader", self.npk.pck_header.cnt_idName)
        self.assertEqual(36, self.npk.pck_header.cnt_payloadLen)
        self.assertEqual(b'gps\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06f-\x06\x97gw]'
                         b'\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00', self.npk.pck_header.cnt_payload)

        self.assertEqual("gps", self.npk.pck_header.cnt_programName)
        self.assertEqual("6.45.6 - rc(?): 102", self.npk.pck_header.cnt_osVersion)
        self.assertEqual(datetime.datetime(2019, 9, 10, 9, 6, 31), self.npk.pck_header.cnt_built_time)
        self.assertEqual((0, 0, 0, 0), self.npk.pck_header.cnt_nullBlock)
        self.assertEqual((0, 0, 0, 0, 2, 0, 0), self.npk.pck_header.cnt_flags)

    def test_ReleaseTyp(self):
        cnt = self.cnt[1]

        self.assertEqual(24, cnt.cnt_id)
        self.assertEqual(50, cnt._offsetInPck)
        self.assertEqual("PckReleaseTyp", cnt.cnt_idName)
        self.assertEqual(6, cnt.cnt_payloadLen)
        self.assertEqual(b"stable", cnt.cnt_payload)
        self.assertEqual(12, cnt.cnt_fullLength)

    def test_PckArchitectureTag(self):
        cnt = self.cnt[2]

        self.assertEqual(16, cnt.cnt_id)
        self.assertEqual(62, cnt._offsetInPck)
        self.assertEqual("CntArchitectureTag", cnt.cnt_idName)
        self.assertEqual(4, cnt.cnt_payloadLen)
        self.assertEqual(b"i386", cnt.cnt_payload)
        self.assertEqual(10, cnt.cnt_fullLength)

    def test_PckDescription(self):
        cnt = self.cnt[3]

        self.assertEqual(2, cnt.cnt_id)
        self.assertEqual(72, cnt._offsetInPck)
        self.assertEqual("PckDescription", cnt.cnt_idName)
        self.assertEqual(25, cnt.cnt_payloadLen)
        self.assertEqual(b'Provides support for GPS.', cnt.cnt_payload)
        self.assertEqual(31, cnt.cnt_fullLength)

    def test_PckHash(self):
        cnt = self.cnt[4]

        self.assertEqual(23, cnt.cnt_id)
        self.assertEqual(103, cnt._offsetInPck)
        self.assertEqual("PckEckcdsaHash", cnt.cnt_idName)
        self.assertEqual(40, cnt.cnt_payloadLen)
        self.assertEqual(b'1a7d206bbfe626c55aa6d2d2caabb6a5a990f13d', cnt.cnt_payload)
        self.assertEqual(46, cnt.cnt_fullLength)

    def test_PckRequirementsHeader(self):
        cnt = self.cnt[5]

        self.assertEqual(3, cnt.cnt_id)
        self.assertEqual(149, cnt._offsetInPck)
        self.assertEqual("PckRequirementsHeader", cnt.cnt_idName)
        self.assertEqual(1, cnt.cnt_structure_id)
        self.assertEqual(34, cnt.cnt_payloadLen)
        self.assertEqual('system', cnt.cnt_programName)
        self.assertEqual((0, 0, 0, 0), cnt.cnt_nullBlock)
        self.assertEqual("6.45.6 - rc(?): 102", cnt.cnt_osVersionFrom)
        self.assertEqual("6.45.6 - rc(?): 102", cnt.cnt_osVersionTo)
        self.assertEqual("<not available for version 0,1>", cnt.cnt_flags)
        self.assertEqual(40, cnt.cnt_fullLength)

    def test_PckNullBlock(self):
        cnt = self.cnt[6]

        self.assertEqual(22, cnt.cnt_id)
        self.assertEqual(189, cnt._offsetInPck)
        self.assertEqual("CntNullBlock", cnt.cnt_idName)
        self.assertEqual(3895, cnt.cnt_payloadLen)
        self.assertEqual(b'\x00' * 3895, cnt.cnt_payload)
        self.assertEqual(3901, cnt.cnt_fullLength)

    def test_PckSquashFsImage(self):
        cnt = self.cnt[7]

        self.assertEqual(21, cnt.cnt_id)
        self.assertEqual(4090, cnt._offsetInPck)
        self.assertEqual("CntSquashFsImage", cnt.cnt_idName)
        self.assertEqual(49152, cnt.cnt_payloadLen)
        self.assertEqual(b'hsqs', cnt.cnt_payload[0:4])
        self.assertEqual(49158, cnt.cnt_fullLength)

    def test_PckSquashFsHashSignature(self):
        cnt = self.cnt[8]

        self.assertEqual(9, cnt.cnt_id)
        self.assertEqual(53248, cnt._offsetInPck)
        self.assertEqual("CntSquashFsHashSignature", cnt.cnt_idName)
        self.assertEqual(68, cnt.cnt_payloadLen)
        self.assertEqual(b'\x8e\xa2\xb1\x8e\xf7n\xef355', cnt.cnt_payload[0:10])
        self.assertEqual(74, cnt.cnt_fullLength)

    def test_parseGpsFilxe_PckArchitectureTag_Closing(self):
        cnt = self.cnt[9]

        self.assertEqual(16, cnt.cnt_id)
        self.assertEqual(53322, cnt._offsetInPck)
        self.assertEqual("CntArchitectureTag", cnt.cnt_idName)
        self.assertEqual(1, cnt.cnt_payloadLen)
        self.assertEqual(b'I', cnt.cnt_payload[0:10])
        self.assertEqual(7, cnt.cnt_fullLength)

    def test_checkStructure(self):
        self.assertEqual(10, len(self.npk.pck_cntList))
        self.assertEqual([1, 24, 16, 2, 23, 3, 22, 21, 9, 16], list(cnt.cnt_id for cnt in self.npk.pck_cntList))


class WriteModifiedGpsFile_Test(GpsFile_Test):
    def test_modify_PckRequirementsHeader(self):
        x = b"\x03\x00\x22\x00\x00\x00\x01\x00\x73\x79\x73\x74\x65\x6d\x00\x00" + \
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x06\x66\x2d\x06\x00\x00\x00\x00" + \
            b"\x06\x66\x2d\x06\x00\x00\x00\x00"

        cnt = None
        for c in self.cnt:
            if c.cnt_id == 3:
                cnt = c
                break

        self.assertEqual(x, cnt.cnt_fullBinary)

    def test_createFile_changePayloadTwice(self):
        oldPayload = self.npk.pck_header.cnt_payload

        self.npk.pck_header.cnt_payload = b"A"
        self.npk.pck_header.cnt_payload = oldPayload

        self.assertEqual(Npk(self.npkFile).file.read_bytes(), self.npk.pck_fullBinary)
