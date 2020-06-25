import unittest

from npkpy.npk.pck_release_typ import PckReleaseTyp
from tests.constants import get_dummy_basic_cnt


class Test_pckReleaseTyp(unittest.TestCase):
    def setUp(self) -> None:
        self.cnt = PckReleaseTyp(get_dummy_basic_cnt(cnt_id=24), offset_in_pck=0)

    def test_validate_cnt_id(self):
        self.assertEqual(24, self.cnt.cnt_id)
