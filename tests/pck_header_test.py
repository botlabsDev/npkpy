import datetime
import struct
import unittest

from npkpy.npk.pck_header import PckHeader
from tests.constants import DummyHeaderCnt


class Test_pckHeader(unittest.TestCase):
    def setUp(self) -> None:
        self.dummy_cnt = DummyHeaderCnt()
        self.dummy_cnt._00_cnt_id = struct.pack("h", 1)
        self.cnt = PckHeader(self.dummy_cnt.get_binary, offset_in_pck=0)

    def test_validateCntId(self):
        self.assertEqual(1, self.cnt.cnt_id)

    def test_getCntProgramName(self):
        self.assertEqual("01234567890abcde", self.cnt.cnt_program_name)

    def test_getOsVersion(self):
        self.assertEqual("1.2.3 - rc(?): 4", self.cnt.cnt_os_version)

    def test_getNullBlock(self):
        self.assertEqual((0, 0, 0, 0), self.cnt.cnt_null_block)

    def test_getBuildTime(self):
        self.assertEqual(datetime.datetime(1970, 1, 1, 0, 0, 1), self.cnt.cnt_built_time)

    def test_getOutput(self):
        self.assertEqual(('PckHeader',
                          ['Cnt id:           1',
                           'Cnt offset:       0',
                           'Cnt len:          41',
                           'Payload len:      35',
                           "Payload[0:10]:    b'0123456789' [...] ",
                           'Program name:     01234567890abcde',
                           'Os version:       1.2.3 - rc(?): 4',
                           'Created at:       1970-01-01 00:00:01',
                           'NullBlock:        (0, 0, 0, 0)',
                           'Flags:            (0, 0, 0, 0, 0, 0, 0)']), self.cnt.output_cnt)

    def test_getCntFlags(self):
        self.assertEqual((0, 0, 0, 0, 0, 0, 0), self.cnt.cnt_flags)

    def test_flagsForSpecificVersion(self):
        # INFO: pkt with version 5.23 seems to have only four flags.
        cnt = PckHeader(self.dummy_cnt.get_binary_with_special_flags, offset_in_pck=0)
        self.assertEqual((0, 0, 0, 0), cnt.cnt_flags)
