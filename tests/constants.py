# HEADER
import struct

from npkpy.npk.pck_header import NPK_PCK_HEADER

MAGIC_BYTES = b"\x1e\xf1\xd0\xba"

PCKSIZE = struct.pack("I", 28)
MAGIC_AND_SIZE = MAGIC_BYTES + PCKSIZE

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


def get_dummy_npk_binary(cnt=None):
    if not cnt:
        cnt = DummyHeaderCnt().get_binary
    pckPayload = cnt
    pckLen = struct.pack("I", len(pckPayload))
    npkBinary = MAGIC_BYTES + pckLen + pckPayload
    return npkBinary


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
    _09b_cnt_flagsB = struct.pack("4B", 0, 0, 0, 0)

    _02_payload = _02_cnt_programName + \
                  _03_cnt_versionRevision + \
                  _04_cnt_versionRc + \
                  _05_cnt_versionMinor + \
                  _06_cnt_versionMajor + \
                  _07_cnt_buildTime + \
                  _08_cnt_nullBock + \
                  _09a_cnt_flagsA

    _02_payloadSpecialFlag = _02_cnt_programName + \
                             _03_cnt_versionRevision + \
                             _04_cnt_versionRc + \
                             _05_cnt_versionMinor + \
                             _06_cnt_versionMajor + \
                             _07_cnt_buildTime + \
                             _08_cnt_nullBock + \
                             _09b_cnt_flagsB

    @property
    def get_binary(self):
        return self._00_cnt_id + \
               self._01_cnt_payload_len + \
               self._02_payload

    @property
    def get_binary_with_special_flags(self):
        return self._00_cnt_id + \
               self._01_cnt_payload_len + \
               self._02_payloadSpecialFlag


class DummyRequirementsHeader:
    _00_cnt_id = struct.pack("H", 3)
    _01_cnt_payload_len = struct.pack("I", 35)
    _02_cnt_struct_id = struct.pack("H", 0)
    _03_cnt_program_name = struct.pack("16s", b"abcdefghijklmnop")

    _04_cnt_min_versionRevision = struct.pack("B", 3)
    _05_cnt_min_versionRc = struct.pack("B", 4)
    _06_cnt_min_versionMinor = struct.pack("B", 2)
    _07_cnt_min_versionMajor = struct.pack("B", 1)

    _08_cnt_nullBock = struct.pack("I", 0)

    _09_cnt_max_versionRevision = struct.pack("B", 7)
    _10_cnt_max_versionRc = struct.pack("B", 8)
    _11_cnt_max_versionMinor = struct.pack("B", 6)
    _12_cnt_max_versionMajor = struct.pack("B", 5)

    _13_cnt_flags = struct.pack("5B", 0, 0, 0, 0, 0)

    def __init__(self, structId):
        self._02_cnt_struct_id = struct.pack(b"H", structId)

    @property
    def get_binary(self):
        return (self._00_cnt_id +
                self._01_cnt_payload_len +
                self._02_payload
                )

    @property
    def _02_payload(self):
        return (self._02_cnt_struct_id +
                self._03_cnt_program_name +
                self._04_cnt_min_versionRevision +
                self._05_cnt_min_versionRc +
                self._06_cnt_min_versionMinor +
                self._07_cnt_min_versionMajor +
                self._08_cnt_nullBock +
                self._09_cnt_max_versionRevision +
                self._10_cnt_max_versionRc +
                self._11_cnt_max_versionMinor +
                self._12_cnt_max_versionMajor +
                self._13_cnt_flags
                )


class DummyBasicCnt:
    _00_cnt_id = struct.pack("h", -1)
    _02_cnt_payload = struct.pack("7s", b"Payload")
    _01_cnt_payload_len = struct.pack("I", len(_02_cnt_payload))

    @property
    def cnt_full_binary(self):
        return self._00_cnt_id + \
               self._01_cnt_payload_len + \
               self._02_cnt_payload


class DummyMulticontainer_Header:
    payload = b"d" * 28 + b"0" * 4
    _00_cnt_id = struct.pack("h", 18)
    _01_cnt_payload_len = struct.pack("I", len(payload))
    _02_cnt_payload = struct.pack(f"{len(payload)}s", payload)

    @property
    def cnt_full_binary(self):
        return self._00_cnt_id + \
               self._01_cnt_payload_len + \
               self._02_cnt_payload
