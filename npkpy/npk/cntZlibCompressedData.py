from npkpy.npk.cntBasic import NpkContainerBasic

NPK_ZLIB_COMPRESSED_DATA = 4


class CntZlibCompressedData(NpkContainerBasic):
    @property
    def _regularCntId(self):
        return NPK_ZLIB_COMPRESSED_DATA
