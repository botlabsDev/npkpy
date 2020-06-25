import re
from pathlib import Path

from npkpy.common import sha1_sum_from_file

ARCHITECTURES = ['arm', 'mipsbe', 'mipsle', 'mmips', 'ppc', 'smips', 'tile', 'x86']

RE_NPK_SUFFIX = '\\.(npk$)'
RE_VERSION = '([\\d]+[\\.\\d]*\\d)'
RE_PROGRAM_NAME = '(^[\\w-]*)-'


class FileBasic:
    __data = None

    def __init__(self, file_path: Path):
        self.file = file_path

    @property
    def filename_suffix(self):
        suffix = re.search(RE_NPK_SUFFIX, self.file.name)
        return suffix.group(1) if suffix else "<NoSuffixMatch>"

    @property
    def filename_version(self):
        result = re.search(RE_VERSION, self.file.name)
        return result.group(1) if result else "<NoVersionMatch>"

    @property
    def filename_architecture(self):
        for arch in ARCHITECTURES:
            if f"-{arch}.npk" in self.file.name:
                return arch
        return "x86"

    @property
    def filename_program_name(self):
        name = re.search(RE_PROGRAM_NAME, self.file.name)
        if name:
            return name.group(1).replace(f"_{self.filename_architecture}_", "")
        return "<NoProgramNameMatch>"

    @property
    def file_hash(self):
        return sha1_sum_from_file(self.file)

    def read_data_from_file(self, offset, size):
        with self.file.open("rb") as _file:
            _file.seek(offset)
            return bytearray(_file.read(size))
