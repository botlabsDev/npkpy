import struct
import unittest

from npkpy.npk.XCntMultiContainerList import XCnt_MultiContainerList
from tests.constants import DummyBasicCnt


class Test_xCnt_MultiContainerList(unittest.TestCase):
    def setUp(self) -> None:
        dummyCnt = DummyBasicCnt()
        dummyCnt._00_cnt_id = struct.pack("h", 20)

        self.cnt = XCnt_MultiContainerList(dummyCnt.binCnt, offsetInPck=0)

    def test_validateCntId(self):
        self.assertEqual(20, self.cnt.cnt_id)
