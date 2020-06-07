from npkpy.npk.cntBasic import NpkContainerBasic

NPK_SQUASHFS_HASH_SIGNATURE = 9


class CntSquashFsHashSignature(NpkContainerBasic):
    @property
    def _regularCntId(self):
        return NPK_SQUASHFS_HASH_SIGNATURE

    @property
    def output_cnt(self):
        idName, options = super().output_cnt
        return idName, options + [f"Payload[-10:]:    {self.cnt_payload[-10:]}"]
