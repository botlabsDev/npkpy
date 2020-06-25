import logging
import struct

from npkpy.common import NPKError

BYTES_LEN_CNT_ID = 2
BYTES_LEN_CNT_PAYLOAD_LEN = 4

NPK_CNT_BASIC = -1


class CntBasic:
    """
        0____4____8____b____f
        |    |    |    |    |
    x0_|AABB|BBCC|C ..... C|
    x1_|....|....|....|....|

    A = Container Identifier
    B = Payload length
    C = Payload
    """

    def __init__(self, data, offset_in_pck):
        self._data = bytearray(data)
        self._offset_in_pck = offset_in_pck
        self.modified = False

    @property
    def _regular_cnt_id(self):
        return NPK_CNT_BASIC

    @property
    def cnt_id(self):
        cnt_id = struct.unpack_from(b"h", self._data, 0)[0]
        if cnt_id != self._regular_cnt_id:
            raise NPKError(f"Cnt object does not represent given container typ {self._regular_cnt_id}/{cnt_id}")
        return cnt_id

    @property
    def cnt_id_name(self):
        return str(self.__class__.__name__)

    @property
    def cnt_payload_len(self):
        return (struct.unpack_from(b"I", self._data, 2))[0]

    @cnt_payload_len.setter
    def cnt_payload_len(self, payload_len):
        logging.warning("[MODIFICATION] Please be aware that modifications can break the npk structure")
        self.modified = True
        struct.pack_into(b"I", self._data, 2, payload_len)

    @property
    def cnt_payload(self):
        return struct.unpack_from(f"{self.cnt_payload_len}s", self._data, 6)[0]

    @cnt_payload.setter
    def cnt_payload(self, payload):
        tmp_len = len(payload)
        tmp_head = self._data[:2 + 4]
        tmp_head += struct.pack(f"{tmp_len}s", payload)
        self._data = tmp_head
        self.cnt_payload_len = tmp_len

    @property
    def cnt_full_length(self):
        return BYTES_LEN_CNT_ID + BYTES_LEN_CNT_PAYLOAD_LEN + self.cnt_payload_len
        # return len(self._data)

    @property
    def output_cnt(self):
        view_len = min(10, self.cnt_payload_len)

        return (f"{self.cnt_id_name}", [f"Cnt id:           {self.cnt_id}",
                                        f"Cnt offset:       {self._offset_in_pck}",
                                        f"Cnt len:          {self.cnt_full_length}",
                                        f"Payload len:      {self.cnt_payload_len}",
                                        f"Payload[0:{view_len}]:    {self.cnt_payload[0:view_len]} [...] "
                                        ])

    @property
    def cnt_full_binary(self):
        cnt_id = self.cnt_id
        payload_len = self.cnt_payload_len

        payload = struct.unpack_from(f"{self.cnt_payload_len}s",
                                     buffer=self._data,
                                     offset=BYTES_LEN_CNT_ID + BYTES_LEN_CNT_PAYLOAD_LEN)[0]

        return struct.pack(b"=hI", cnt_id, payload_len) + payload
