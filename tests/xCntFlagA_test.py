import struct
import unittest

from npkpy.npk.xCntFlagA import XCnt_flagA
from tests.constants import DummyBasicCnt


class Test_xCnt_flagB(unittest.TestCase):
    def setUp(self) -> None:
        dummyCnt = DummyBasicCnt()
        dummyCnt._00_cnt_id = struct.pack("h", 7)

        self.cnt = XCnt_flagA(dummyCnt.binCnt, offsetInPck=0)

    def test_validateCntId(self):
        self.assertEqual(7, self.cnt.cnt_id)

