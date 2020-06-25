import struct
import unittest

from npkpy.npk.cnt_flag_c import CntFlagC
from tests.constants import DummyBasicCnt


class Test_cntFlagC(unittest.TestCase):
    def setUp(self) -> None:
        dummyCnt = DummyBasicCnt()
        dummyCnt._00_cnt_id = struct.pack("h", 17)

        self.cnt = CntFlagC(dummyCnt.cnt_full_binary, offset_in_pck=0)

    def test_validateCntId(self):
        self.assertEqual(17, self.cnt.cnt_id)
