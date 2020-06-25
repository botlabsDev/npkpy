import datetime
import struct

from npkpy.npk.cnt_basic import CntBasic

NPK_PCK_HEADER = 1

"""
    0____4____8____b____f
    |    |    |    |    |
 x0_|AABB|BBCC|CCCC|CCCC|
 x1_|CCCC|CCDE|FGHH|HH..|
 x2_|....|....|....|....|

A = Container Identifier (2)
B = Payload length (4)
C = Program Name (16)
D = Program version: revision
E = Program version: rc
F = Program version: minor
G = Program version: major
H = Build time
I = NULL BLock / Flags

"""


class PckHeader(CntBasic):
    def __init__(self, data, offset_in_pck):
        super().__init__(data, offset_in_pck)
        self._offset = offset_in_pck
        self.flag_offset = 0

    @property
    def _regular_cnt_id(self):
        return NPK_PCK_HEADER

    @property
    def cnt_program_name(self):
        return bytes(struct.unpack_from("16B", self._data, 6)).decode().rstrip('\x00')

    @property
    def cnt_os_version(self):
        revision = (struct.unpack_from("B", self._data, 22))[0]
        unknown_subrevision = (struct.unpack_from("B", self._data, 23))[0]
        minor = (struct.unpack_from("B", self._data, 24))[0]
        major = (struct.unpack_from("B", self._data, 25))[0]
        return f"{major}.{minor}.{revision} - rc(?): {unknown_subrevision}"

    @property
    def cnt_built_time(self):
        return datetime.datetime.utcfromtimestamp(struct.unpack_from("I", self._data, 26)[0])

    @property
    def cnt_null_block(self):
        return struct.unpack_from("4B", self._data, 30)

    @property
    def cnt_flags(self):
        try:
            return struct.unpack_from("7B", self._data, 34)
        except struct.error:
            # INFO: pkt with version 5.23 seems to have only four flags.
            return struct.unpack_from("4B", self._data, 34)

    @property
    def output_cnt(self):
        id_name, options = super().output_cnt
        return (id_name, options + [f"Program name:     {self.cnt_program_name}",
                                    f"Os version:       {self.cnt_os_version}",
                                    f"Created at:       {self.cnt_built_time}",
                                    f"NullBlock:        {self.cnt_null_block}",
                                    f"Flags:            {self.cnt_flags}"
                                    ])
