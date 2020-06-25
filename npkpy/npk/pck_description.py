from npkpy.npk.cnt_basic import CntBasic

NPK_PCK_DESCRIPTION = 2


class PckDescription(CntBasic):
    @property
    def _regular_cnt_id(self):
        return NPK_PCK_DESCRIPTION
