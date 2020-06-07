from npkpy.common import sha1sumFromBinary
from npkpy.npk.cntBasic import NpkContainerBasic

NPK_SQUASH_FS_IMAGE = 21


class CntSquashFsImage(NpkContainerBasic):
    @property
    def _regularCntId(self):
        return NPK_SQUASH_FS_IMAGE

    @property
    def cnt_payload_hash(self):
        return sha1sumFromBinary(self.cnt_payload)

    @property
    def output_cnt(self):
        idName, options = super().output_cnt
        return idName, options + [f"calc Sha1Hash:    {self.cnt_payload_hash}"]
