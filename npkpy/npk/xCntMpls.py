from npkpy.npk.pckRequirementsHeader import PckRequirementsHeader

NPK_MPLS = 19


class XCntMpls(PckRequirementsHeader):
    @property
    def _regularCntId(self):
        return NPK_MPLS
