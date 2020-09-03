import struct
from pathlib import Path

from npkpy.common import NPKError, NPKIdError, NPKMagicBytesError
from npkpy.npk.npk_constants import CNT_HANDLER
from npkpy.npk.cnt_basic import BYTES_LEN_CNT_ID, BYTES_LEN_CNT_PAYLOAD_LEN
from npkpy.npk.npk_file_basic import FileBasic

MAGIC_BYTES = b"\x1e\xf1\xd0\xba"
BYTES_LEN_MAGIC_HEADER = 4
BYTES_LEN_PCK_SIZE_LEN = 4

"""
  0____4____8____b____f
  |    |    |    |    |
0_|AAAA|BBBB| C ..... |
1_|....|....|....|....|


A = MAGIC BYTES (4)
B = PCK SIZE (4)
C = Begin of Container area

"""


class Npk(FileBasic):
    __cnt_list = None

    def __init__(self, file_path: Path):
        super().__init__(file_path)
        self.cnt_offset = 8
        self._data = self.read_data_from_file(offset=0, size=self.cnt_offset)
        self._check_magic_bytes(error_msg="Magic bytes not found in Npk file")
        self.pck_header = self.pck_cnt_list[0]

    @property
    def pck_magic_bytes(self):
        return struct.unpack_from("4s", self._data, 0)[0]

    @property
    def pck_payload_len(self):
        self.__pck_payload_size_update()
        payload_len = struct.unpack_from("I", self._data, 4)[0]
        return payload_len

    def __pck_payload_size_update(self):
        if any(cnt.modified for cnt in self.pck_cnt_list):
            current_size = 0
            for cnt in self.pck_cnt_list:
                current_size += cnt.cnt_full_length
                cnt.modified = False
            struct.pack_into("I", self._data, 4, current_size)

    @property
    def pck_full_size(self):
        return BYTES_LEN_MAGIC_HEADER + BYTES_LEN_PCK_SIZE_LEN + self.pck_payload_len

    @property
    def pck_full_binary(self):
        binary = MAGIC_BYTES + struct.pack("I", self.pck_payload_len)
        for cnt in self.pck_cnt_list:
            binary += cnt.cnt_full_binary
        return binary

    @property
    def pck_enumerate_cnt(self):
        for pos, cnt in enumerate(self.pck_cnt_list):
            yield pos, cnt

    @property
    def pck_cnt_list(self):
        if not self.__cnt_list:
            self.__cnt_list = self.__parse_all_cnt()
        return self.__cnt_list

    def __parse_all_cnt(self):
        lst = []
        offset = self.cnt_offset
        while offset < self.file.stat().st_size - 1:
            lst.append(self.__get_cnt(offset))
            offset += BYTES_LEN_CNT_ID + BYTES_LEN_CNT_PAYLOAD_LEN + lst[-1].cnt_payload_len
        return lst

    def __get_cnt(self, offset):
        cnt_id = struct.unpack_from("H", self.read_data_from_file(offset, 2))[0]
        payload_len = struct.unpack_from("I", self.read_data_from_file(offset + BYTES_LEN_CNT_ID, 4))[0]
        pkt_len = BYTES_LEN_CNT_ID + BYTES_LEN_CNT_PAYLOAD_LEN + payload_len

        data = self.read_data_from_file(offset, pkt_len)
        if len(data) != pkt_len:
            raise NPKError(f"File maybe corrupted. Please download again. File: {self.file.absolute()}")
        try:
            return CNT_HANDLER[cnt_id](data, offset)
        except KeyError as e:
            raise NPKIdError(f"Failed with cnt id: {cnt_id}\n"
                             f"New cnt id discovered in file: {self.file.absolute()}") from e


    def _check_magic_bytes(self, error_msg):
        if not self.pck_magic_bytes == MAGIC_BYTES:
            raise NPKMagicBytesError(error_msg)
