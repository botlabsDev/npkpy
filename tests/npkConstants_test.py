import unittest

from npkpy.npk.npkConstants import CNT_HANDLER
from tests.constants import DummyBasicCnt


class Test_npkConstants(unittest.TestCase):

    def test_validateAssignment_DictIdIsContainerId(self):
        for cnt_id, cnt_class in CNT_HANDLER.items():
            if cnt_class != "?":
                cnt = cnt_class(DummyBasicCnt().binCnt, 0)
                self.assertEqual(cnt_id, cnt._regularCntId,
                                 msg=f"{cnt_id}!={cnt._regularCntId}")
