from npkpy.npk.cnt_basic import CntBasic

NPK_FLAG_A = 7


class CntFlagA(CntBasic):
    @property
    def _regular_cnt_id(self):
        return NPK_FLAG_A
