import struct
import unittest

from npkpy.npk.cntBasic import NpkContainerBasic
from tests.constants import DummyBasicCnt


class Test_npkContainerBasic(unittest.TestCase):

    def setUp(self) -> None:
        self.cnt = NpkContainerBasic(DummyBasicCnt().binCnt, offsetInPck=0)

    def test_extractCntId(self):
        self.assertEqual(-1, self.cnt.cnt_id)

    def test_failForWrongCntId(self):
        dummyCnt = DummyBasicCnt()
        dummyCnt._00_cnt_id = struct.pack("h", 999)
        cnt = NpkContainerBasic(dummyCnt.binCnt, offsetInPck=0)
        with self.assertRaises(RuntimeError) as e:
            _ = cnt.cnt_id
        self.assertEqual("Cnt object does not represent given container typ -1/999", e.exception.args[0])

    def test_getNameOfContainerType(self):
        self.assertEqual("NpkContainerBasic", self.cnt.cnt_idName)

    def test_extractPayloadLen(self):
        self.assertEqual(7, self.cnt.cnt_payloadLen)

    def test_extractPayload(self):
        self.assertEqual(b"Payload", self.cnt.cnt_payload)

    def test_extractCntFromGivenOffset(self):
        self.assertEqual(len(DummyBasicCnt().binCnt), self.cnt.cnt_fullLength)

    def test_giveOverviewOfCnt(self):
        expectedResult = ('NpkContainerBasic', [f'Cnt id:           -1',
                                                'Cnt offset:       0',
                                                'Cnt len:          13',
                                                'Payload len:      7',
                                                "Payload[0:7]:    b'Payload' [...] "])
        self.assertEqual(expectedResult, self.cnt.output_cnt)

    def test_getFullBinaryOfContainer(self):
        self.assertEqual(DummyBasicCnt().binCnt, self.cnt.cnt_fullBinary)


class Test_modifyNpkContainerBasic(unittest.TestCase):
    def setUp(self) -> None:
        self.cnt = NpkContainerBasic(DummyBasicCnt().binCnt, offsetInPck=0)

    def test_increaseCntSize(self):
        origCntFullLength = self.cnt.cnt_fullLength
        origPayloadLen = self.cnt.cnt_payloadLen

        self.cnt.cnt_payloadLen += 3

        self.assertEqual(7, origPayloadLen)
        self.assertEqual(10, self.cnt.cnt_payloadLen)
        self.assertEqual(13, origCntFullLength)
        self.assertEqual(16, self.cnt.cnt_fullLength)

    def test_decreaseCntSize(self):
        origCntFullLength = self.cnt.cnt_fullLength
        origPayloadLen = self.cnt.cnt_payloadLen

        self.cnt.cnt_payloadLen -= 4

        self.assertEqual(7, origPayloadLen)
        self.assertEqual(13, origCntFullLength)
        self.assertEqual(3, self.cnt.cnt_payloadLen)
        self.assertEqual(9, self.cnt.cnt_fullLength)

    def test_failAccessPayload_afterIncreasingPayloadLenField(self):
        origPayloadLen = self.cnt.cnt_payloadLen
        self.cnt.cnt_payloadLen += 3

        self.assertEqual(origPayloadLen + 3, self.cnt.cnt_payloadLen)
        with self.assertRaises(struct.error):
            _ = self.cnt.cnt_payload

    def test_decreasingPayloadLenField_decreaseFullCntLenAndPayload(self):
        origCntFullLength = self.cnt.cnt_fullLength
        origPayloadLen = self.cnt.cnt_payloadLen

        self.cnt.cnt_payloadLen -= 4

        self.assertEqual(origPayloadLen - 4, self.cnt.cnt_payloadLen)
        self.assertEqual(origCntFullLength - 4, self.cnt.cnt_fullLength)
        self.assertEqual(b"Pay", self.cnt.cnt_payload)

    def test_failDecreasingPayloadLenFieldBelowZero(self):
        with self.assertRaises(struct.error) as e:
            self.cnt.cnt_payloadLen -= 8
        self.assertEqual("argument out of range", e.exception.args[0])

    def test_increasePayload_updatePayloadLen(self):
        replacingPayload = b"NewTestPayload"

        self.cnt.cnt_payload = replacingPayload

        self.assertEqual(replacingPayload, self.cnt.cnt_payload)
        self.assertEqual(len(replacingPayload), self.cnt.cnt_payloadLen)

    def test_decreasePayload_updatePayloadLen(self):
        replacingPayload = b"New"

        self.cnt.cnt_payload = replacingPayload
        self.assertEqual(replacingPayload, self.cnt.cnt_payload)
        self.assertEqual(len(replacingPayload), self.cnt.cnt_payloadLen)

    def test_NullPayload_updatePayloadLenToZero(self):
        replacingPayload = b""

        self.cnt.cnt_payload = replacingPayload
        self.assertEqual(replacingPayload, self.cnt.cnt_payload)
        self.assertEqual(len(replacingPayload), self.cnt.cnt_payloadLen)

