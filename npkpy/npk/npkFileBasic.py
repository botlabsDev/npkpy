import re
from pathlib import Path

from npkpy.common import sha1sumFromFile

ARCHITECTURES = ['arm', 'mipsbe', 'mipsle', 'mmips', 'ppc', 'smips', 'tile', 'x86']

RE_SUFFIX = '\.(npk$)'
RE_VERSION = '-(\d\.\d\d\.\d)'
RE_PROGRAM_NAME = '(^[\w-]*)-'


class FileBasic:
    __data = None

    def __init__(self, filePath: Path):
        self.file = filePath

    @property
    def filename_suffix(self):
        return re.search(RE_SUFFIX, self.file.name).group(1)

    @property
    def filename_version(self):
        return re.search(RE_VERSION, self.file.name).group(1)

    @property
    def filename_architecture(self):
        for a in ARCHITECTURES:
            if f"_{a}_" in self.file.name:
                return a
        return "x86"

    @property
    def filename_program(self):
        name = re.search(RE_PROGRAM_NAME, self.file.name).group(1)
        name.replace(f"_{self.filename_architecture}_", "")
        return name

    @property
    def file_hash(self):
        return sha1sumFromFile(self.file)

    def readDataFromFile(self, offset, size):
        with self.file.open("rb") as f:
            f.seek(offset)
            return bytearray(f.read(size))
