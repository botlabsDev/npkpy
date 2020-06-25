from npkpy.npk.cnt_basic import CntBasic

NPK_FLAG_B = 8


class CntFlagB(CntBasic):
    """
    Flag typ found in gps-5.23-mipsbe.npk
    Payload contains b'\n    update-console\n  '
    """

    @property
    def _regular_cnt_id(self):
        return NPK_FLAG_B
