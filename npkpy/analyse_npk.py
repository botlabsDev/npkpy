from npkpy.common import get_full_pkt_info, extract_container
from npkpy.npk.cnt_squasfs_image import NPK_SQUASH_FS_IMAGE
from npkpy.npk.cnt_zlib_compressed_data import NPK_ZLIB_COMPRESSED_DATA
from npkpy.npk.npk_constants import CNT_HANDLER

EXPORT_FOLDER_PREFIX = "npkPyExport_"


def analyse_npk(opts, npk_files):
    filter_container = []

    if opts.show_container:
        for file in npk_files:
            print("\n".join(get_full_pkt_info(file)))

    if opts.export_all:
        print("export all!!")
        filter_container = CNT_HANDLER.keys()
    if opts.export_squashfs:
        filter_container = [NPK_SQUASH_FS_IMAGE]
    if opts.export_zlib:
        filter_container = [NPK_ZLIB_COMPRESSED_DATA]

    if filter_container:
        for npk_file in npk_files:
            export_folder = opts.dst_folder / f"{EXPORT_FOLDER_PREFIX}{npk_file.file.stem}"
            export_folder.mkdir(parents=True, exist_ok=True)

            extract_container(npk_file, export_folder, filter_container)

            if not next(export_folder.iterdir(), None):
                export_folder.rmdir()
