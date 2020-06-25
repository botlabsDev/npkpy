import unittest

from npkpy.npk.pck_eckcdsa_hash import PckEckcdsaHash
from tests.constants import get_dummy_basic_cnt


class Test_pckEckcdsaHash(unittest.TestCase):
    def setUp(self) -> None:
        self.cnt = PckEckcdsaHash(get_dummy_basic_cnt(cnt_id=23), offset_in_pck=0)

    def test_validateCntId(self):
        self.assertEqual(23, self.cnt.cnt_id)
