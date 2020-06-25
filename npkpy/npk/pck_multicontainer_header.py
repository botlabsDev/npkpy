import struct

from npkpy.npk.pck_header import PckHeader

NPK_MULTICONTAINER_HEADER: int = 18


class PktMulticontainerHeader(PckHeader):
    @property
    def _regular_cnt_id(self):
        return NPK_MULTICONTAINER_HEADER

    @property
    def cnt_flags(self):
        return struct.unpack_from(b"4B", self._data, 34)
