from npkpy.npk.pck_multicontainer_list import NPK_MULTICONTAINER_LIST, PktMulticontainerList
from npkpy.npk.cnt_architecture_tag import NPK_ARCHITECTURE_TAG, CntArchitectureTag
from npkpy.npk.cnt_null_block import NPK_NULL_BLOCK, CntNullBlock
from npkpy.npk.pck_release_typ import NPK_RELEASE_TYP, PckReleaseTyp
from npkpy.npk.cnt_squasfs_image import NPK_SQUASH_FS_IMAGE, CntSquashFsImage
from npkpy.npk.cnt_squashfs_hash_signature import NPK_SQUASHFS_HASH_SIGNATURE, CntSquashFsHashSignature
from npkpy.npk.cnt_zlib_compressed_data import NPK_ZLIB_COMPRESSED_DATA, CntZlibDompressedData
from npkpy.npk.cnt_basic import NPK_CNT_BASIC, CntBasic
from npkpy.npk.pck_description import NPK_PCK_DESCRIPTION, PckDescription
from npkpy.npk.pck_eckcdsa_hash import NPK_ECKCDSA_HASH, PckEckcdsaHash
from npkpy.npk.pck_header import NPK_PCK_HEADER, PckHeader
from npkpy.npk.pck_requirements_header import NPK_REQUIREMENTS_HEADER, PckRequirementsHeader
from npkpy.npk.cnt_flag_b import NPK_FLAG_B, CntFlagB
from npkpy.npk.cnt_flag_c import NPK_FLAG_C, CntFlagC
from npkpy.npk.cnt_flag_a import NPK_FLAG_A, CntFlagA
from npkpy.npk.pck_multicontainer_header import NPK_MULTICONTAINER_HEADER, PktMulticontainerHeader
from npkpy.npk.cnt_mpls import NPK_MPLS, CntMpls



CNT_HANDLER = {
    NPK_CNT_BASIC: CntBasic,
    0: "?",
    NPK_PCK_HEADER: PckHeader,
    NPK_PCK_DESCRIPTION: PckDescription,
    NPK_REQUIREMENTS_HEADER: PckRequirementsHeader,
    NPK_ZLIB_COMPRESSED_DATA: CntZlibDompressedData,
    5: "?",
    6: "?",
    NPK_FLAG_A: CntFlagA,
    NPK_FLAG_B: CntFlagB,
    NPK_SQUASHFS_HASH_SIGNATURE: CntSquashFsHashSignature,
    10: "?",
    11: "?",
    12: "?",
    13: "?",
    14: "?",
    15: "?",
    NPK_ARCHITECTURE_TAG: CntArchitectureTag,
    NPK_FLAG_C: CntFlagC,
    NPK_MULTICONTAINER_HEADER: PktMulticontainerHeader,
    NPK_MPLS: CntMpls,
    NPK_MULTICONTAINER_LIST: PktMulticontainerList,
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
