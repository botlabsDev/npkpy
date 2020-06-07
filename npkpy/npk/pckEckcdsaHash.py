from npkpy.npk.cntBasic import NpkContainerBasic

NPK_ECKCDSA_HASH = 23
class PckEckcdsaHash(NpkContainerBasic):
    @property
    def _regularCntId(self):
        return NPK_ECKCDSA_HASH


