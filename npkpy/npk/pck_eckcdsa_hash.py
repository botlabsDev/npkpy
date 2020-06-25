from npkpy.npk.cnt_basic import CntBasic

NPK_ECKCDSA_HASH = 23


class PckEckcdsaHash(CntBasic):
    @property
    def _regular_cnt_id(self):
        return NPK_ECKCDSA_HASH
