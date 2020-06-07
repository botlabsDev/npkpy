from npkpy.npk.cntBasic import NpkContainerBasic

NPK_PCK_DESCRIPTION = 2
class PckDescription(NpkContainerBasic):
    @property
    def _regularCntId(self):
        return NPK_PCK_DESCRIPTION
