from npkpy.npk.cntBasic import NpkContainerBasic

NPK_FLAG_C = 17


class XCnt_flagC(NpkContainerBasic):
    ##TODO: found in multicast-3.30-mipsbe.npk
    @property
    def _regularCntId(self):
        return NPK_FLAG_C

    # @property
    # def cnt_payload(self):
    #     # TODO pkt gps-5.23-mipsbe.npk contains  b'\n    update-console\n  '
