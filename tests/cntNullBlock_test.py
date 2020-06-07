import struct
import unittest

from npkpy.npk.cntNullBlock import CntNullBlock
from tests.constants import DummyBasicCnt


class Test_cntNullBlock(unittest.TestCase):
    def setUp(self) -> None:
        dummyCnt = DummyBasicCnt()
        dummyCnt._00_cnt_id = struct.pack("h", 22)

        self.cnt = CntNullBlock(dummyCnt.binCnt, offsetInPck=0)

    def test_validateCntId(self):
        self.assertEqual(22, self.cnt.cnt_id)
