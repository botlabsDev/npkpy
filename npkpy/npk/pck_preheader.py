from npkpy.npk.cnt_basic import CntBasic

NPK_PCK_PREHEADER = 25

class PckPreHeader(CntBasic):
    @property
    def _regular_cnt_id(self):
        return NPK_PCK_PREHEADER
