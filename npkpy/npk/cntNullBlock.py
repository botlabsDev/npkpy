from npkpy.npk.cntBasic import NpkContainerBasic

NPK_NULL_BLOCK = 22


class CntNullBlock(NpkContainerBasic):
    @property
    def _regularCntId(self):
        return NPK_NULL_BLOCK
