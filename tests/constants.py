# HEADER
import struct

from npkpy.npk.pckHeader import NPK_PCK_HEADER

MAGICBYTES = b"\x1e\xf1\xd0\xba"

PCKSIZE = struct.pack("I", 28)
MAGIC_AND_SIZE = MAGICBYTES + PCKSIZE

# OPENING ARCHITECTURE_TAG
SET_HEADER_TAG_ID = struct.pack("H", NPK_PCK_HEADER)  # b"\x01\x00"
SET_HEADER_TAG_PAYLOAD = bytes("NAME OF PROGRAM".encode())
SET_HEADER_TAG_SIZE = struct.pack("I", len(SET_HEADER_TAG_PAYLOAD))

CNT_SET_ARCHITECTURE_TAG = SET_HEADER_TAG_ID + \
                           SET_HEADER_TAG_SIZE + \
                           SET_HEADER_TAG_PAYLOAD

# CLOSING ARCHITECTURE_TAG
CLOSING_ARCHITECTURE_TAG_ID = struct.pack("H", 1)  # b"\x01\x00"
CLOSING_ARCHITECTURE_TAG_PAYLOAD = struct.pack("s", b"I")
CLOSING_ARCHITECTURE_TAG_SIZE = struct.pack("I", len(CLOSING_ARCHITECTURE_TAG_PAYLOAD))

CNT_CLOSING_ARCHITECTURE_TAG = CLOSING_ARCHITECTURE_TAG_ID + \
                               CLOSING_ARCHITECTURE_TAG_SIZE + \
                               CLOSING_ARCHITECTURE_TAG_PAYLOAD

# MINIMAL_NPK_PAKAGE


MINIMAL_NPK_PACKAGE = MAGIC_AND_SIZE + \
                      CNT_SET_ARCHITECTURE_TAG + \
                      CNT_CLOSING_ARCHITECTURE_TAG


def getDummyNpkBinary(payload=None):
    if not payload:
        payload = DummyHeaderCnt().binHeaderCntA
    pckPayload = payload
    pckLen = struct.pack("I", len(pckPayload))
    npkBinary = MAGICBYTES + pckLen + pckPayload
    return npkBinary


class DummyBasicCnt:
    _00_cnt_id = struct.pack("h", -1)
    _01_cnt_payload_len = struct.pack("I", 7)
    _02_cnt_payload = struct.pack("7s", b"Payload")

    @property
    def binCnt(self):
        return self._00_cnt_id + \
               self._01_cnt_payload_len + \
               self._02_cnt_payload


class DummyHeaderCnt:
    _00_cnt_id = struct.pack("H", 1)
    _01_cnt_payload_len = struct.pack("I", 35)
    _02_cnt_programName = struct.pack("16s", b"01234567890abcdef")
    _03_cnt_versionRevision = struct.pack("B", 3)
    _04_cnt_versionRc = struct.pack("B", 4)
    _05_cnt_versionMinor = struct.pack("B", 2)
    _06_cnt_versionMajor = struct.pack("B", 1)
    _07_cnt_buildTime = struct.pack("I", 1)
    _08_cnt_nullBock = struct.pack("I", 0)
    _09a_cnt_flagsA = struct.pack("7B", 0, 0, 0, 0, 0, 0, 0)
    # _09b_cnt_flagsB = struct.pack("4B", 0, 0, 0, 0)

    @property
    def binHeaderCntA(self):
        return self._binBasicHeaderCnt + self._09a_cnt_flagsA

    # @property
    # def binHeaderCntB(self):
    #     return self._binBasicHeaderCnt + self._09b_cnt_flagsB

    @property
    def _binBasicHeaderCnt(self):
        return self._00_cnt_id + \
               self._01_cnt_payload_len + \
               self._02_cnt_programName + \
               self._03_cnt_versionRevision + \
               self._04_cnt_versionRc + \
               self._05_cnt_versionMinor + \
               self._06_cnt_versionMajor + \
               self._07_cnt_buildTime + \
               self._08_cnt_nullBock
