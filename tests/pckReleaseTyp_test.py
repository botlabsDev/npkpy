import struct
import unittest

from npkpy.npk.pckReleaseTyp import PckReleaseTyp
from tests.constants import DummyBasicCnt


class Test_pckReleaseTyp(unittest.TestCase):
    def setUp(self) -> None:
        dummyCnt = DummyBasicCnt()
        dummyCnt._00_cnt_id = struct.pack("h", 24)

        self.cnt = PckReleaseTyp(dummyCnt.binCnt, offsetInPck=0)

    def test_validateCntId(self):
        self.assertEqual(24, self.cnt.cnt_id)
