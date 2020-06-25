from npkpy.npk.cnt_basic import CntBasic

NPK_NULL_BLOCK = 22


class CntNullBlock(CntBasic):
    @property
    def _regular_cnt_id(self):
        return NPK_NULL_BLOCK
