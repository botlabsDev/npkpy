import struct
import unittest

from npkpy.npk.cnt_zlib_compressed_data import CntZlibDompressedData
from tests.constants import DummyBasicCnt


class Test_cntZlibCompressedData(unittest.TestCase):
    def setUp(self) -> None:
        dummyCnt = DummyBasicCnt()
        dummyCnt._00_cnt_id = struct.pack("h", 4)
        self.cnt = CntZlibDompressedData(dummyCnt.cnt_full_binary, offset_in_pck=0)

    def test_validateCntId(self):
        self.assertEqual(4, self.cnt.cnt_id)
