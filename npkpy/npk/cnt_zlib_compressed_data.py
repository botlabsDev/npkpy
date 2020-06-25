from npkpy.npk.cnt_basic import CntBasic

NPK_ZLIB_COMPRESSED_DATA = 4


class CntZlibDompressedData(CntBasic):
    @property
    def _regular_cnt_id(self):
        return NPK_ZLIB_COMPRESSED_DATA
