import struct
import unittest

from npkpy.npk.pck_release_typ import PckReleaseTyp
from tests.constants import DummyBasicCnt


class Test_pckReleaseTyp(unittest.TestCase):
    def setUp(self) -> None:
        dummy_cnt = DummyBasicCnt()
        dummy_cnt._00_cnt_id = struct.pack("h", 24)

        self.cnt = PckReleaseTyp(dummy_cnt.cnt_full_binary, offset_in_pck=0)

    def test_validate_cnt_id(self):
        self.assertEqual(24, self.cnt.cnt_id)
