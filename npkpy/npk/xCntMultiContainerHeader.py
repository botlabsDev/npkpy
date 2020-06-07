import struct

from npkpy.npk.pckHeader import PckHeader

NPK_MULTICONTAINER_HEADER: int = 18


class XCnt_multiContainerHeader(PckHeader):
    @property
    def _regularCntId(self):
        return NPK_MULTICONTAINER_HEADER

    @property
    def cnt_flags(self):
        return struct.unpack_from(b"4B", self._data, 34)
