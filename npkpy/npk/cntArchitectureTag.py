from npkpy.npk.cntBasic import NpkContainerBasic

NPK_ARCHITECTURE_TAG = 16


class CntArchitectureTag(NpkContainerBasic):
    @property
    def _regularCntId(self):
        return NPK_ARCHITECTURE_TAG
