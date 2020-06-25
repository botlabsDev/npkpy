import unittest

from npkpy.npk.cnt_zlib_compressed_data import CntZlibDompressedData
from tests.constants import get_dummy_basic_cnt


class Test_cntZlibCompressedData(unittest.TestCase):
    def setUp(self) -> None:
        self.cnt = CntZlibDompressedData(get_dummy_basic_cnt(cnt_id=4), offset_in_pck=0)

    def test_validateCntId(self):
        self.assertEqual(4, self.cnt.cnt_id)
