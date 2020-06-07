import struct
import unittest

from npkpy.npk.xCntFlagC import XCnt_flagC
from tests.constants import DummyBasicCnt


class Test_xCnt_flagC(unittest.TestCase):
    def setUp(self) -> None:
        dummyCnt = DummyBasicCnt()
        dummyCnt._00_cnt_id = struct.pack("h", 17)

        self.cnt = XCnt_flagC(dummyCnt.binCnt, offsetInPck=0)

    def test_validateCntId(self):
        self.assertEqual(17, self.cnt.cnt_id)

