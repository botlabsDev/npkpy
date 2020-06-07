from npkpy.npk.cntBasic import NpkContainerBasic

NPK_RELEASE_TYP = 24


class PckReleaseTyp(NpkContainerBasic):
    @property
    def _regularCntId(self):
        return NPK_RELEASE_TYP