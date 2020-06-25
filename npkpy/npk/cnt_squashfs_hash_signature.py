from npkpy.npk.cnt_basic import CntBasic

NPK_SQUASHFS_HASH_SIGNATURE = 9


class CntSquashFsHashSignature(CntBasic):
    @property
    def _regular_cnt_id(self):
        return NPK_SQUASHFS_HASH_SIGNATURE

    @property
    def output_cnt(self):
        id_name, options = super().output_cnt
        return id_name, options + [f"Payload[-10:]:    {self.cnt_payload[-10:]}"]
