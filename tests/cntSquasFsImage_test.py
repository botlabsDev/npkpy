import struct
import unittest

from npkpy.npk.cntSquasFsImage import CntSquashFsImage
from tests.constants import DummyBasicCnt


class Test_cntSquashFsImage(unittest.TestCase):
    def setUp(self) -> None:
        dummyCnt = DummyBasicCnt()
        dummyCnt._00_cnt_id = struct.pack("h", 21)
        self.cnt = CntSquashFsImage(dummyCnt.binCnt, offsetInPck=0)

        self.expectedHash = b'\xc3\x04\x15\xea\xccjYDit\xb7\x16\xef\xf5l\xf2\x82\x19\x81]'

    def test_validateCntId(self):
        self.assertEqual(21, self.cnt.cnt_id)

    def test_payload_hash(self):
        self.assertEqual(self.expectedHash, self.cnt.cnt_payload_hash)

    def test_giveOverviewOfCnt(self):
        expected = f"calc Sha1Hash:    {self.expectedHash}"

        _, cntData = self.cnt.output_cnt

        self.assertEqual(expected, cntData[-1])
