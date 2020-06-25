from npkpy.npk.cnt_basic import CntBasic

NPK_FLAG_C = 17


class CntFlagC(CntBasic):
    """
    Flag typ only found in multicast-3.30-mipsbe.npk
    """

    @property
    def _regular_cnt_id(self):
        return NPK_FLAG_C
