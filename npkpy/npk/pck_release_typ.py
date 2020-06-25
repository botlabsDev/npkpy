from npkpy.npk.cnt_basic import CntBasic

NPK_RELEASE_TYP = 24


class PckReleaseTyp(CntBasic):
    @property
    def _regular_cnt_id(self):
        return NPK_RELEASE_TYP
