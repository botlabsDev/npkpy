import struct
import unittest

from npkpy.npk.cntSquashFsHashSignature import CntSquashFsHashSignature
from tests.constants import DummyBasicCnt


class Test_cntSquashFsHashSignature(unittest.TestCase):
    def setUp(self) -> None:
        dummyCnt = DummyBasicCnt()
        dummyCnt._00_cnt_id = struct.pack("h", 9)
        self.cnt = CntSquashFsHashSignature(dummyCnt.binCnt, offsetInPck=0)

    def test_validateCntId(self):
        self.assertEqual(9, self.cnt.cnt_id)

    def test_giveOverviewOfCnt(self):
        expected = "Payload[-10:]:    b'Payload'"

        _, cntData = self.cnt.output_cnt

        self.assertEqual(expected, cntData[-1])
