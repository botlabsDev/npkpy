import unittest

from npkpy.npk.npk_constants import CNT_HANDLER
from tests.constants import DummyBasicCnt


class Test_npkConstants(unittest.TestCase):

    def test_validateAssignment_DictIdIsContainerId(self):
        for cnt_id, cnt_class in CNT_HANDLER.items():
            if cnt_class != "?":
                cnt = cnt_class(DummyBasicCnt().cnt_full_binary, 0)
                self.assertEqual(cnt_id, cnt._regular_cnt_id,
                                 msg=f"{cnt_id}!={cnt._regular_cnt_id}")
