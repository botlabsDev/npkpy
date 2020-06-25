import unittest

from npkpy.npk.cnt_flag_c import CntFlagC
from tests.constants import get_dummy_basic_cnt


class Test_cntFlagC(unittest.TestCase):
    def setUp(self) -> None:
        self.cnt = CntFlagC(get_dummy_basic_cnt(cnt_id=17), offset_in_pck=0)

    def test_validateCntId(self):
        self.assertEqual(17, self.cnt.cnt_id)
