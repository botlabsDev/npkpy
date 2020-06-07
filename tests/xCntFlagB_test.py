import struct
import unittest

from npkpy.npk.xCntFlagB import XCnt_flagB
from tests.constants import DummyBasicCnt


class Test_xCnt_flagB(unittest.TestCase):
    def setUp(self) -> None:
        dummyCnt = DummyBasicCnt()
        dummyCnt._00_cnt_id = struct.pack("h", 8)

        self.cnt = XCnt_flagB(dummyCnt.binCnt, offsetInPck=0)

    def test_validateCntId(self):
        self.assertEqual(8, self.cnt.cnt_id)


