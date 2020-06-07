import datetime
import struct

from npkpy.npk.cntBasic import NpkContainerBasic

NPK_PCK_HEADER = 1


class PckHeader(NpkContainerBasic):
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


    def __init__(self, data, offsetInPck):
        super().__init__(data, offsetInPck)
        self._offset = offsetInPck
        self.flagOffset = 0

    @property
    def _regularCntId(self):
        return NPK_PCK_HEADER

    @property
    def cnt_programName(self):
        # TODO: b"" - b needs to be removed!
        return bytes(struct.unpack_from(b"16B", self._data, 6)).decode().rstrip('\x00')

    @property
    def cnt_osVersion(self):
        revision = (struct.unpack_from(b"B", self._data, 22))[0]
        rc = (struct.unpack_from(b"B", self._data, 23))[0]
        minor = (struct.unpack_from(b"B", self._data, 24))[0]
        major = (struct.unpack_from(b"B", self._data, 25))[0]
        return f"{major}.{minor}.{revision} - rc(?): {rc}"

    @property
    def cnt_built_time(self):
        return datetime.datetime.utcfromtimestamp(struct.unpack_from(b"I", self._data, 26)[0])

    @property
    def cnt_nullBlock(self):
        return struct.unpack_from(b"4B", self._data, 30)

    @property
    def cnt_flags(self):
        try:
            return struct.unpack_from(b"7B", self._data, 34)
        except struct.error:
            ## pkt with version 5.23 seems to have only four flags.
            return struct.unpack_from(b"4B", self._data, 34)

    @property
    def output_cnt(self):
        idName, options = super().output_cnt
        return (idName, options + [f"Program name:     {self.cnt_programName}",
                                   f"Os version:       {self.cnt_osVersion}",
                                   f"Created at:       {self.cnt_built_time}",
                                   f"NullBlock:        {self.cnt_nullBlock}",
                                   f"Flags:            {self.cnt_flags}"
                                   ])
