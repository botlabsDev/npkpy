import unittest

from npkpy.npk.cnt_squashfs_hash_signature import CntSquashFsHashSignature
from tests.constants import get_dummy_basic_cnt


class Test_cntSquashFsHashSignature(unittest.TestCase):
    def setUp(self) -> None:
        self.cnt = CntSquashFsHashSignature(get_dummy_basic_cnt(cnt_id=9), offset_in_pck=0)

    def test_validateCntId(self):
        self.assertEqual(9, self.cnt.cnt_id)

    def test_giveOverviewOfCnt(self):
        expected = "Payload[-10:]:    b'Payload'"

        _, cntData = self.cnt.output_cnt

        self.assertEqual(expected, cntData[-1])
