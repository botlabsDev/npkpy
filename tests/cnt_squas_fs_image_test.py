import unittest

from npkpy.npk.cnt_squasfs_image import CntSquashFsImage
from tests.constants import get_dummy_basic_cnt


class Test_cntSquashFsImage(unittest.TestCase):
    def setUp(self) -> None:
        self.cnt = CntSquashFsImage(get_dummy_basic_cnt(cnt_id=21), offset_in_pck=0)

        self.expectedHash = b'\xc3\x04\x15\xea\xccjYDit\xb7\x16\xef\xf5l\xf2\x82\x19\x81]'

    def test_validateCntId(self):
        self.assertEqual(21, self.cnt.cnt_id)

    def test_payloadHash(self):
        self.assertEqual(self.expectedHash, self.cnt.cnt_payload_hash)

    def test_giveOverviewOfCnt(self):
        expected = f"calc Sha1Hash:    {self.expectedHash}"

        _, cntData = self.cnt.output_cnt

        self.assertEqual(expected, cntData[-1])
