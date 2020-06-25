import struct
import unittest

from npkpy.npk.pck_multicontainer_list import PktMulticontainerList
from tests.constants import DummyBasicCnt


class Test_cnt_MultiContainerList(unittest.TestCase):
    def setUp(self) -> None:
        dummy_cnt = DummyBasicCnt()
        dummy_cnt._00_cnt_id = struct.pack("h", 20)

        self.cnt = PktMulticontainerList(dummy_cnt.cnt_full_binary, offset_in_pck=0)

    def test_validateCntId(self):
        self.assertEqual(20, self.cnt.cnt_id)
