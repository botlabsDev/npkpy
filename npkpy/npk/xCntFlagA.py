from npkpy.npk.cntBasic import NpkContainerBasic

NPK_FLAG_A = 7


class XCnt_flagA(NpkContainerBasic):
    @property
    def _regularCntId(self):
        return NPK_FLAG_A

    # @property
    # def cnt_payload(self):
    #     # TODO pkt gps-5.23-mipsbe.npk contains  b'\n    update-console\n  '

