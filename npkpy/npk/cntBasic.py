import logging
import struct

BYTES_LEN_CNT_ID = 2
BYTES_LEN_CNT_PAYLOAD_LEN = 4

NPK_CNT_BASIC = -1


class NpkContainerBasic:
    """
        0____4____8____b____f
        |    |    |    |    |
    x0_|AABB|BBCC|C ..... C|
    x1_|....|....|....|....|

    A = Container Identifier
    B = Payload length
    C = Payload
    """

    def __init__(self, data, offsetInPck):
        self._data = bytearray(data)
        self._offsetInPck = offsetInPck
        self.modified = False

    @property
    def _regularCntId(self):
        return NPK_CNT_BASIC

    @property
    def cnt_id(self):
        cntId = struct.unpack_from(b"h", self._data, 0)[0]
        if cntId != self._regularCntId:
            raise RuntimeError(f"Cnt object does not represent given container typ {self._regularCntId}/{cntId}")
        return cntId

    @property
    def cnt_idName(self):
        return str(self.__class__.__name__)

    @property
    def cnt_payloadLen(self):
        return (struct.unpack_from(b"I", self._data, 2))[0]

    @cnt_payloadLen.setter
    def cnt_payloadLen(self, payloadLen):
        logging.warning("[MODIFICATION] Please be aware that modifications can break the npk structure")
        self.modified = True
        struct.pack_into(b"I", self._data, 2, payloadLen)

    @property
    def cnt_payload(self):
        return struct.unpack_from(f"{self.cnt_payloadLen}s", self._data, 6)[0]

    @cnt_payload.setter
    def cnt_payload(self, payload):
        tmpLen = len(payload)
        tmpHead = self._data[:2 + 4]
        tmpHead += struct.pack(f"{tmpLen}s", payload)
        self._data = tmpHead
        self.cnt_payloadLen = tmpLen

    @property
    def cnt_fullLength(self):
        return BYTES_LEN_CNT_ID + BYTES_LEN_CNT_PAYLOAD_LEN + self.cnt_payloadLen
        # return len(self._data)

    @property
    def output_cnt(self):
        viewLen = min(10, self.cnt_payloadLen)

        return (f"{self.cnt_idName}", [f"Cnt id:           {self.cnt_id}",
                                       f"Cnt offset:       {self._offsetInPck}",
                                       f"Cnt len:          {self.cnt_fullLength}",
                                       f"Payload len:      {self.cnt_payloadLen}",
                                       f"Payload[0:{viewLen}]:    {self.cnt_payload[0:viewLen]} [...] "
                                       ])

    @property
    def cnt_fullBinary(self):
        cntId = self.cnt_id
        payloadLen = self.cnt_payloadLen

        payload = struct.unpack_from(f"{self.cnt_payloadLen}s",
                                     buffer=self._data,
                                     offset=BYTES_LEN_CNT_ID + BYTES_LEN_CNT_PAYLOAD_LEN)[0]

        return struct.pack(b"=hI", cntId, payloadLen) + payload
