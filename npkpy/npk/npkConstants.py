from npkpy.npk.XCntMultiContainerList import NPK_MULTICONTAINER_LIST, XCnt_MultiContainerList
from npkpy.npk.cntArchitectureTag import NPK_ARCHITECTURE_TAG, CntArchitectureTag
from npkpy.npk.cntNullBlock import NPK_NULL_BLOCK, CntNullBlock
from npkpy.npk.pckReleaseTyp import NPK_RELEASE_TYP, PckReleaseTyp
from npkpy.npk.cntSquasFsImage import NPK_SQUASH_FS_IMAGE, CntSquashFsImage
from npkpy.npk.cntSquashFsHashSignature import NPK_SQUASHFS_HASH_SIGNATURE, CntSquashFsHashSignature
from npkpy.npk.cntZlibCompressedData import NPK_ZLIB_COMPRESSED_DATA, CntZlibCompressedData
from npkpy.npk.cntBasic import NPK_CNT_BASIC, NpkContainerBasic
from npkpy.npk.pckDescription import NPK_PCK_DESCRIPTION, PckDescription
from npkpy.npk.pckEckcdsaHash import NPK_ECKCDSA_HASH, PckEckcdsaHash
from npkpy.npk.pckHeader import NPK_PCK_HEADER, PckHeader
from npkpy.npk.pckRequirementsHeader import NPK_REQUIREMENTS_HEADER, PckRequirementsHeader
from npkpy.npk.xCntFlagB import NPK_FLAG_B, XCnt_flagB
from npkpy.npk.xCntFlagC import NPK_FLAG_C, XCnt_flagC
from npkpy.npk.xCntFlagA import NPK_FLAG_A, XCnt_flagA
from npkpy.npk.xCntMultiContainerHeader import NPK_MULTICONTAINER_HEADER, XCnt_multiContainerHeader
from npkpy.npk.xCntMpls import NPK_MPLS, XCntMpls



CNT_HANDLER = {
    NPK_CNT_BASIC: NpkContainerBasic,
    0: "?",
    NPK_PCK_HEADER: PckHeader,
    NPK_PCK_DESCRIPTION: PckDescription,
    NPK_REQUIREMENTS_HEADER: PckRequirementsHeader,
    NPK_ZLIB_COMPRESSED_DATA: CntZlibCompressedData,
    5: "?",
    6: "?",
    NPK_FLAG_A: XCnt_flagA,
    NPK_FLAG_B: XCnt_flagB,
    NPK_SQUASHFS_HASH_SIGNATURE: CntSquashFsHashSignature,
    10: "?",
    11: "?",
    12: "?",
    13: "?",
    14: "?",
    15: "?",
    NPK_ARCHITECTURE_TAG: CntArchitectureTag,
    NPK_FLAG_C: XCnt_flagC,
    NPK_MULTICONTAINER_HEADER: XCnt_multiContainerHeader,
    NPK_MPLS: XCntMpls,
    NPK_MULTICONTAINER_LIST: XCnt_MultiContainerList,
    NPK_SQUASH_FS_IMAGE: CntSquashFsImage,
    NPK_NULL_BLOCK: CntNullBlock,
    NPK_ECKCDSA_HASH: PckEckcdsaHash,
    NPK_RELEASE_TYP: PckReleaseTyp,
    25: "?",
    26: "?",
    27: "?",
    28: "?",
    29: "?",
    30: "?",
}
