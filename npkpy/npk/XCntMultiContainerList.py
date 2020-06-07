from npkpy.npk.pckRequirementsHeader import PckRequirementsHeader

NPK_MULTICONTAINER_LIST = 20


class XCnt_MultiContainerList(PckRequirementsHeader):
    @property
    def _regularCntId(self):
        return NPK_MULTICONTAINER_LIST
