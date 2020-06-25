import unittest

from npkpy.npk.pck_description import PckDescription
from tests.constants import get_dummy_basic_cnt


class Test_pckDescription(unittest.TestCase):
    def setUp(self) -> None:
        self.cnt = PckDescription(get_dummy_basic_cnt(cnt_id=2), offset_in_pck=0)

    def test_validateCntId(self):
        self.assertEqual(2, self.cnt.cnt_id)
