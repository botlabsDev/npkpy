import unittest

from npkpy.npk.npk_constants import CNT_HANDLER
from tests.constants import get_dummy_basic_cnt


class Test_npkConstants(unittest.TestCase):

    def test_validateAssignment_DictIdIsContainerId(self):
        for cnt_id, cnt_class in CNT_HANDLER.items():
            if cnt_class != "?":
                cnt = cnt_class(get_dummy_basic_cnt(), 0)
                self.assertEqual(cnt_id, cnt._regular_cnt_id,
                                 msg=f"{cnt_id}!={cnt._regular_cnt_id}")
