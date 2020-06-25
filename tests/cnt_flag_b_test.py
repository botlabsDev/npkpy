import struct
import unittest

from npkpy.npk.cnt_flag_b import CntFlagB
from tests.constants import DummyBasicCnt


class Test_cntFlagB(unittest.TestCase):
    def setUp(self) -> None:
        dummyCnt = DummyBasicCnt()
        dummyCnt._00_cnt_id = struct.pack("h", 8)

        self.cnt = CntFlagB(dummyCnt.cnt_full_binary, offset_in_pck=0)

    def test_validateCntId(self):
        self.assertEqual(8, self.cnt.cnt_id)
