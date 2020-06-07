import tempfile
import unittest
from pathlib import Path

from tests.constants import MINIMAL_NPK_PACKAGE
from npkpy.npk.npk import Npk


class BasicNpkTestRequirements(unittest.TestCase):
    def setUp(self) -> None:
        self.testNpk = Path(tempfile.NamedTemporaryFile().name)
        self.testNpk.write_bytes(MINIMAL_NPK_PACKAGE)
        self.npk = Npk(self.testNpk)

    def tearDown(self) -> None:
        self.testNpk.unlink()


class ParseTestPackage_Test(BasicNpkTestRequirements):
    def test_minimalNPK_parseHeader(self):
        self.assertEqual(b"\x1e\xf1\xd0\xba", self.npk.pck_magicBytes)
        self.assertEqual(28, self.npk.pck_payloadLen)

    def test_minimalNPK_parseAllContainer(self):
        listOfCnt = self.npk.pck_cntList

        self.assertEqual(1, listOfCnt[0].cnt_id)
        self.assertEqual(15, listOfCnt[0].cnt_payloadLen)
        self.assertEqual(b"NAME OF PROGRAM", listOfCnt[0].cnt_payload)
        self.assertEqual(1, listOfCnt[1].cnt_id)
        self.assertEqual(1, listOfCnt[1].cnt_payloadLen)
        self.assertEqual(b"I", listOfCnt[1].cnt_payload)


class ModifyPayload_Test(BasicNpkTestRequirements):

    def setUp(self) -> None:
        super().setUp()
        self.cnt = self.npk.pck_cntList[0]

    def test_emptyPayload_emptyContainer(self):
        self.cnt.cnt_payload = b""

        self.assertEqual(1, self.cnt.cnt_id)
        self.assertEqual(0, self.cnt.cnt_payloadLen)
        self.assertEqual(b"", self.cnt.cnt_payload)
        self.assertEqual(6, self.cnt.cnt_fullLength)

        self.assertEqual(13, self.npk.pck_payloadLen)
        self.assertEqual(21, self.npk.pck_fullSize)

    def test_dontchangePayloadSize_recalculateContainerKeepSize(self):
        self.cnt.cnt_payload = b"PROGRAM OF NAME"

        self.assertEqual(1, self.cnt.cnt_id)
        self.assertEqual(15, self.cnt.cnt_payloadLen)
        self.assertEqual(b"PROGRAM OF NAME", self.cnt.cnt_payload)
        self.assertEqual(21, self.cnt.cnt_fullLength)

        self.assertEqual(28, self.npk.pck_payloadLen)
        self.assertEqual(36, self.npk.pck_fullSize)

    def test_increasePayloadLen_recalculateContainerSizeBigger(self):
        self.cnt.cnt_payload = b"NEW NAME OF PROGRAM"

        self.assertEqual(1, self.cnt.cnt_id)
        self.assertEqual(19, self.cnt.cnt_payloadLen)
        self.assertEqual(b"NEW NAME OF PROGRAM", self.cnt.cnt_payload)
        self.assertEqual(25, self.cnt.cnt_fullLength)

        self.assertEqual(32, self.npk.pck_payloadLen)
        self.assertEqual(40, self.npk.pck_fullSize)

    def test_decreasePayloadLen_recalculateContainerSmaller(self):
        self.cnt.cnt_payload = b"SHORT NAME"

        self.assertEqual(1, self.cnt.cnt_id)
        self.assertEqual(10, self.cnt.cnt_payloadLen)
        self.assertEqual(b"SHORT NAME", self.cnt.cnt_payload)
        self.assertEqual(16, self.cnt.cnt_fullLength)

        self.assertEqual(23, self.npk.pck_payloadLen)
        self.assertEqual(31, self.npk.pck_fullSize)


class WriteModifiedFile_Test(BasicNpkTestRequirements):
    def setUp(self) -> None:
        super().setUp()
        self.cnt = self.npk.pck_cntList[0]

    def test_createFile_withoutModification(self):
        self.assertEqual(MINIMAL_NPK_PACKAGE, self.npk.pck_fullBinary)

    def test_createFile_changePayloadTwice(self):
        self.cnt.cnt_payload = b"A"
        self.cnt.cnt_payload = b"NAME OF PROGRAM"
        self.assertEqual(MINIMAL_NPK_PACKAGE, self.npk.pck_fullBinary)
