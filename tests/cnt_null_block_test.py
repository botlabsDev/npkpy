import unittest

from npkpy.npk.cnt_null_block import CntNullBlock
from tests.constants import get_dummy_basic_cnt


class Test_cntNullBlock(unittest.TestCase):
    def setUp(self) -> None:
        self.cnt = CntNullBlock(get_dummy_basic_cnt(cnt_id=22), offset_in_pck=0)

    def test_validateCntId(self):
        self.assertEqual(22, self.cnt.cnt_id)
