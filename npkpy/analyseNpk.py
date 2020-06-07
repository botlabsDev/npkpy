from npkpy.common import getFullPktInfo, extractContainer
from npkpy.npk.cntSquasFsImage import NPK_SQUASH_FS_IMAGE
from npkpy.npk.cntZlibCompressedData import NPK_ZLIB_COMPRESSED_DATA
from npkpy.npk.npkConstants import CNT_HANDLER

EXPORT_FOLDER_PREFIX = "npkPyExport_"


def analyseNpk(opts, npkFiles):
    filterContainer = []

    if opts.showContainer:
        for file in npkFiles:
            print("\n".join(getFullPktInfo(file)))

    if opts.exportAll:
        filterContainer = CNT_HANDLER.keys()
    if opts.exportSquashFs:
        filterContainer = [NPK_SQUASH_FS_IMAGE]
    if opts.exportZlib:
        filterContainer = [NPK_ZLIB_COMPRESSED_DATA]

    if filterContainer:
        for npkFile in npkFiles:
            exportFolder = opts.dstFolder / f"{EXPORT_FOLDER_PREFIX}{npkFile.file.stem}"
            exportFolder.mkdir(parents=True, exist_ok=True)

            extractContainer(npkFile, exportFolder, filterContainer)

            if not next(exportFolder.iterdir(), None):
                exportFolder.rmdir()
