import struct
import unittest

from npkpy.npk.pck_multicontainer_header import PktMulticontainerHeader
from tests.constants import DummyHeaderCnt


class Test_pktMultiContainerHeader(unittest.TestCase):
    def setUp(self) -> None:
        dummy_cnt = DummyHeaderCnt()
        dummy_cnt._00_cnt_id = struct.pack("h", 18)
        self.cnt = PktMulticontainerHeader(dummy_cnt.get_binary, offset_in_pck=0)

    def test_validateCntId(self):
        self.assertEqual(18, self.cnt.cnt_id)

    def test_getCntFlags(self):
        self.assertEqual((0, 0, 0, 0), self.cnt.cnt_flags)
