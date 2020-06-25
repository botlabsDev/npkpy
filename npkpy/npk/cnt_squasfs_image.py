from npkpy.common import sha1_sum_from_binary
from npkpy.npk.cnt_basic import CntBasic

NPK_SQUASH_FS_IMAGE = 21


class CntSquashFsImage(CntBasic):
    @property
    def _regular_cnt_id(self):
        return NPK_SQUASH_FS_IMAGE

    @property
    def cnt_payload_hash(self):
        return sha1_sum_from_binary(self.cnt_payload)

    @property
    def output_cnt(self):
        id_name, options = super().output_cnt
        return id_name, options + [f"calc Sha1Hash:    {self.cnt_payload_hash}"]
