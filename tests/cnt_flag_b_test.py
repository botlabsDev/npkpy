import unittest

from npkpy.npk.cnt_flag_b import CntFlagB
from tests.constants import get_dummy_basic_cnt


class Test_cntFlagB(unittest.TestCase):
    def setUp(self) -> None:
        self.cnt = CntFlagB(get_dummy_basic_cnt(cnt_id=8), offset_in_pck=0)

    def test_validateCntId(self):
        self.assertEqual(8, self.cnt.cnt_id)
