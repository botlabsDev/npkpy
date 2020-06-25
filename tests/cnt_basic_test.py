import struct
import unittest

from npkpy.common import NPKError
from npkpy.npk.cnt_basic import CntBasic
from tests.constants import get_dummy_basic_cnt


class Test_CntBasic(unittest.TestCase):

    def setUp(self) -> None:
        self.cnt = CntBasic(data=get_dummy_basic_cnt(), offset_in_pck=0)

    def test_extractCntId(self):
        self.assertEqual(-1, self.cnt.cnt_id)

    def test_failForWrongCntId(self):
        cnt = CntBasic(get_dummy_basic_cnt(cnt_id=999), offset_in_pck=0)
        with self.assertRaises(NPKError) as _exception:
            _ = cnt.cnt_id
        self.assertEqual("Cnt object does not represent given container typ -1/999", _exception.exception.args[0])

    def test_getNameOfContainerType(self):
        self.assertEqual("CntBasic", self.cnt.cnt_id_name)

    def test_extractPayloadLen(self):
        self.assertEqual(7, self.cnt.cnt_payload_len)

    def test_extractPayload(self):
        self.assertEqual(b"Payload", self.cnt.cnt_payload)

    def test_extractCntFromGivenOffset(self):
        self.assertEqual(len(get_dummy_basic_cnt()), self.cnt.cnt_full_length)

    def test_giveOverviewOfCnt(self):
        expected_result = ('CntBasic', ['Cnt id:           -1',
                                        'Cnt offset:       0',
                                        'Cnt len:          13',
                                        'Payload len:      7',
                                        "Payload[0:7]:    b'Payload' [...] "])
        self.assertEqual(expected_result, self.cnt.output_cnt)

    def test_getFullBinaryOfContainer(self):
        self.assertEqual(get_dummy_basic_cnt(), self.cnt.cnt_full_binary)


class Test_modifyNpkContainerBasic(unittest.TestCase):
    def setUp(self) -> None:
        self.cnt = CntBasic(get_dummy_basic_cnt(), offset_in_pck=0)

    def test_increaseCntSize(self):
        orig_cnt_full_length = self.cnt.cnt_full_length
        orig_payload_len = self.cnt.cnt_payload_len

        self.cnt.cnt_payload_len += 3

        self.assertEqual(7, orig_payload_len)
        self.assertEqual(10, self.cnt.cnt_payload_len)
        self.assertEqual(13, orig_cnt_full_length)
        self.assertEqual(16, self.cnt.cnt_full_length)

    def test_decreaseCntSize(self):
        orig_cnt_full_length = self.cnt.cnt_full_length
        orig_payload_len = self.cnt.cnt_payload_len

        self.cnt.cnt_payload_len -= 4

        self.assertEqual(7, orig_payload_len)
        self.assertEqual(13, orig_cnt_full_length)
        self.assertEqual(3, self.cnt.cnt_payload_len)
        self.assertEqual(9, self.cnt.cnt_full_length)

    def test_failAccessPayloadAfterIncreasingPayloadLenField(self):
        orig_payload_len = self.cnt.cnt_payload_len
        self.cnt.cnt_payload_len += 3

        self.assertEqual(orig_payload_len + 3, self.cnt.cnt_payload_len)
        with self.assertRaises(struct.error):
            _ = self.cnt.cnt_payload

    def test_decreasingPayloadLen_fieldDecreaseFullCntLenAndPayload(self):
        orig_cnt_full_length = self.cnt.cnt_full_length
        orig_payload_len = self.cnt.cnt_payload_len

        self.cnt.cnt_payload_len -= 4

        self.assertEqual(orig_payload_len - 4, self.cnt.cnt_payload_len)
        self.assertEqual(orig_cnt_full_length - 4, self.cnt.cnt_full_length)
        self.assertEqual(b"Pay", self.cnt.cnt_payload)

    def test_failDecreasingPayloadLen_fieldBelowZero(self):
        with self.assertRaises(struct.error) as _exception:
            self.cnt.cnt_payload_len -= 8
        self.assertEqual("argument out of range", _exception.exception.args[0])

    def test_increasePayload_updatePayloadLen(self):
        replace_payload = b"NewTestPayload"

        self.cnt.cnt_payload = replace_payload

        self.assertEqual(replace_payload, self.cnt.cnt_payload)
        self.assertEqual(len(replace_payload), self.cnt.cnt_payload_len)

    def test_decreasePayload_updatePayloadLen(self):
        replace_payload = b"New"

        self.cnt.cnt_payload = replace_payload
        self.assertEqual(replace_payload, self.cnt.cnt_payload)
        self.assertEqual(len(replace_payload), self.cnt.cnt_payload_len)

    def test_nullPayloadUpdate_payloadLenToZero(self):
        replace_payload = b""

        self.cnt.cnt_payload = replace_payload
        self.assertEqual(replace_payload, self.cnt.cnt_payload)
        self.assertEqual(len(replace_payload), self.cnt.cnt_payload_len)
