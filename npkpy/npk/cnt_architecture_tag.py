from npkpy.npk.cnt_basic import CntBasic

NPK_ARCHITECTURE_TAG = 16


class CntArchitectureTag(CntBasic):
    @property
    def _regular_cnt_id(self):
        return NPK_ARCHITECTURE_TAG
