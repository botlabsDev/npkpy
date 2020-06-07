import struct
import unittest

from npkpy.npk.xCntMpls import XCntMpls
from tests.constants import DummyBasicCnt


class Test_xCntMpls(unittest.TestCase):
    def setUp(self) -> None:
        dummyCnt = DummyBasicCnt()
        dummyCnt._00_cnt_id = struct.pack("h", 19)

        self.cnt = XCntMpls(dummyCnt.binCnt, offsetInPck=0)

    def test_validateCntId(self):
        self.assertEqual(19, self.cnt.cnt_id)
