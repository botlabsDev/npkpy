import unittest

from npkpy.npk.cnt_mpls import CntMpls
from tests.constants import get_dummy_basic_cnt


class Test_cntMpls(unittest.TestCase):
    def setUp(self) -> None:
        self.cnt = CntMpls(get_dummy_basic_cnt(cnt_id=19), offset_in_pck=0)

    def test_validateCntId(self):
        self.assertEqual(19, self.cnt.cnt_id)
