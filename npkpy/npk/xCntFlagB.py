from npkpy.npk.cntBasic import NpkContainerBasic

NPK_FLAG_B = 8


class XCnt_flagB(NpkContainerBasic):
    # TODO: found in gps-5.23-mipsbe.npk
    @property
    def _regularCntId(self):
        return NPK_FLAG_B

    # @property
    # def cnt_payload(self):
    #     # TODO pkt gps-5.23-mipsbe.npk contains  b'\n    update-console\n  '
