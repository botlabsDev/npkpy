from npkpy.npk.pck_requirements_header import PckRequirementsHeader

NPK_MULTICONTAINER_LIST = 20


class PktMulticontainerList(PckRequirementsHeader):
    @property
    def _regular_cnt_id(self):
        return NPK_MULTICONTAINER_LIST
