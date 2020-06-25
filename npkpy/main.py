import argparse
from pathlib import Path

from npkpy.analyse_npk import analyse_npk
from npkpy.common import get_all_nkp_files
from npkpy.npk.npk import Npk


def parse_args():
    parser = argparse.ArgumentParser(description='npkPy is an unpacking tool for MikroTiks custom NPK container format')

    input_group = parser.add_argument_group("input")
    input_group.add_argument("--files",
                             action='append', type=Path, help="Select one or more files to process")

    input_group.add_argument("--src-folder",
                             type=Path, default=Path("."),
                             help="Process all NPK files found recursively in given source folder.")

    input_filter_group = input_group.add_mutually_exclusive_group()
    input_filter_group.add_argument("--glob",
                                    type=str, default=None,
                                    help="Simple glob. Filter files from --srcFolder which match the given string.")

    output_group = parser.add_argument_group("output")
    output_group.add_argument("--dst-folder",
                              type=Path, default=Path(".") / "exportNpk",
                              help="Extract container into given folder")

    action_group = parser.add_argument_group("actions")
    exclusive_action = action_group.add_mutually_exclusive_group(required=True)
    exclusive_action.add_argument("--show-container",
                                  action="store_true", help="List all container from selected NPK files")
    exclusive_action.add_argument("--export-all",
                                  action="store_true", help="Export all container from selected NPK files")
    exclusive_action.add_argument("--export-squashfs", action="store_true",
                                  help="Export all SquashFs container from selected NPK files")
    exclusive_action.add_argument("--export-zlib",
                                  action="store_true",
                                  help="Export all Zlib compressed container from selected NPK files")
    return parser.parse_args()


def main():
    opts = parse_args()
    files = (Npk(f) for f in (opts.files if opts.files else get_all_nkp_files(opts.src_folder, opts.glob)))
    analyse_npk(opts, files)
