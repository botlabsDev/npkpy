from npkpy.npk.pck_requirements_header import PckRequirementsHeader

NPK_MPLS = 19


class CntMpls(PckRequirementsHeader):
    @property
    def _regular_cnt_id(self):
        return NPK_MPLS
