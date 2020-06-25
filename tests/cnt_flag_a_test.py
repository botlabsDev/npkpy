import struct
import unittest

from npkpy.npk.cnt_flag_a import CntFlagA
from tests.constants import DummyBasicCnt


class Test_cntFlagA(unittest.TestCase):
    def setUp(self) -> None:
        dummyCnt = DummyBasicCnt()
        dummyCnt._00_cnt_id = struct.pack("h", 7)

        self.cnt = CntFlagA(dummyCnt.cnt_full_binary, offset_in_pck=0)

    def test_validateCntId(self):
        self.assertEqual(7, self.cnt.cnt_id)
