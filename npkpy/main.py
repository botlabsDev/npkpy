import argparse
from pathlib import Path

from npkpy.analyseNpk import analyseNpk
from npkpy.common import getAllNkpFiles
from npkpy.npk.npk import Npk


def parseArgs():
    parser = argparse.ArgumentParser(description='npkPy is an unpacking tool for MikroTiks custom NPK container format')

    inputGroup = parser.add_argument_group("input")
    inputGroup.add_argument("--files", action='append', type=Path,
                            help="Select one or more files to process")
    inputGroup.add_argument("--srcFolder", type=Path, default=Path("."),
                            help="Process all NPK files found recursively in given source folder.")

    inputFilterGroup = inputGroup.add_mutually_exclusive_group()
    inputFilterGroup.add_argument("--glob", type=str, default=None,
                                  help="Simple glob. Filter files from --srcFolder which match the given string.")

    outputGroup = parser.add_argument_group("output")
    outputGroup.add_argument("--dstFolder", type=Path, default=Path(".") / "exportNpk",
                             help="Extract container into given folder")

    actionGroup = parser.add_argument_group("actions")
    exclusiveAction = actionGroup.add_mutually_exclusive_group(required=True)
    exclusiveAction.add_argument("--showContainer", action="store_true",
                                 help="List all container from selected NPK files")
    exclusiveAction.add_argument("--exportAll", action="store_true",
                                 help="Export all container from selected NPK files")
    exclusiveAction.add_argument("--exportSquashFs", action="store_true",
                                 help="Export all SquashFs container from selected NPK files")
    exclusiveAction.add_argument("--exportZlib", action="store_true",
                                 help="Export all Zlib compressed container from selected NPK files")

    return parser.parse_args()


def main():
    opts = parseArgs()
    files = (Npk(f) for f in (opts.files if opts.files else getAllNkpFiles(opts.srcFolder, opts.glob)))
    analyseNpk(opts, files)
