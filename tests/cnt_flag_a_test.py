import unittest

from npkpy.npk.cnt_flag_a import CntFlagA
from tests.constants import get_dummy_basic_cnt


class Test_cntFlagA(unittest.TestCase):
    def setUp(self) -> None:
        self.cnt = CntFlagA(get_dummy_basic_cnt(cnt_id=7), offset_in_pck=0)

    def test_validateCntId(self):
        self.assertEqual(7, self.cnt.cnt_id)
