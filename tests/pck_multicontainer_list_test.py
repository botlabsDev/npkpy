import unittest

from npkpy.npk.pck_multicontainer_list import PktMulticontainerList
from tests.constants import get_dummy_basic_cnt


class Test_cnt_MultiContainerList(unittest.TestCase):
    def setUp(self) -> None:
        self.cnt = PktMulticontainerList(get_dummy_basic_cnt(cnt_id=20), offset_in_pck=0)

    def test_validateCntId(self):
        self.assertEqual(20, self.cnt.cnt_id)
