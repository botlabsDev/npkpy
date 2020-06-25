import struct
import unittest

from npkpy.npk.pck_description import PckDescription
from tests.constants import DummyBasicCnt


class Test_pckDescription(unittest.TestCase):
    def setUp(self) -> None:
        dummyCnt = DummyBasicCnt()
        dummyCnt._00_cnt_id = struct.pack("h", 2)

        self.cnt = PckDescription(dummyCnt.cnt_full_binary, offset_in_pck=0)

    def test_validateCntId(self):
        self.assertEqual(2, self.cnt.cnt_id)
