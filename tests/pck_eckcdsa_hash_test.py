import struct
import unittest

from npkpy.npk.pck_eckcdsa_hash import PckEckcdsaHash
from tests.constants import DummyBasicCnt


class Test_pckEckcdsaHash(unittest.TestCase):
    def setUp(self) -> None:
        dummyCnt = DummyBasicCnt()
        dummyCnt._00_cnt_id = struct.pack("h", 23)

        self.cnt = PckEckcdsaHash(dummyCnt.cnt_full_binary, offset_in_pck=0)

    def test_validateCntId(self):
        self.assertEqual(23, self.cnt.cnt_id)