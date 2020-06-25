import struct
import unittest

from npkpy.npk.cnt_mpls import CntMpls
from tests.constants import DummyBasicCnt


class Test_cntMpls(unittest.TestCase):
    def setUp(self) -> None:
        dummyCnt = DummyBasicCnt()
        dummyCnt._00_cnt_id = struct.pack("h", 19)

        self.cnt = CntMpls(dummyCnt.cnt_full_binary, offset_in_pck=0)

    def test_validateCntId(self):
        self.assertEqual(19, self.cnt.cnt_id)
