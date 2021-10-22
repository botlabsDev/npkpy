import unittest

from npkpy.npk.pck_preheader import PckPreHeader
from tests.constants import get_dummy_basic_cnt


class Test_pckPreHeader(unittest.TestCase):
    def setUp(self) -> None:
        self.cnt = PckPreHeader(get_dummy_basic_cnt(cnt_id=25), offset_in_pck=0)

    def test_validateCntId(self):
        self.assertEqual(25, self.cnt.cnt_id)
