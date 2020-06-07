import struct
from pathlib import Path

from npkpy.npk.npkConstants import CNT_HANDLER
from npkpy.npk.cntBasic import BYTES_LEN_CNT_ID, BYTES_LEN_CNT_PAYLOAD_LEN
from npkpy.npk.npkFileBasic import FileBasic

MAGICBYTES = b"\x1e\xf1\xd0\xba"
BYTES_LEN_MAGIC_HEADER = 4
BYTES_LEN_PCK_SIZE_LEN = 4


class Npk(FileBasic):
    """
      0____4____8____b____f
      |    |    |    |    |
    0_|AAAA|BBBB| C ..... |
    1_|....|....|....|....|


    A = MAGIC BYTES (4)
    B = PCK SIZE (4)
    C = Begin of Container area

    """
    __cntList = None

    def __init__(self, filePath: Path):
        super().__init__(filePath)
        self.cntOffset = 8
        self._data = self.readDataFromFile(0, self.cntOffset)
        self._checkMagicBytes(errorMsg="MagicBytes not found in Npk file")
        self.pck_header = self.pck_cntList[0]

    @property
    def pck_magicBytes(self):
        return struct.unpack_from(b"4s", self._data, 0)[0]

    @property
    def pck_payloadLen(self):
        self.__pck_payloadUpdate()
        payloadLen = struct.unpack_from(b"I", self._data, 4)[0]
        return payloadLen

    def __pck_payloadUpdate(self):
        if any(cnt.modified for cnt in self.pck_cntList):
            currentSize = 0
            for cnt in self.pck_cntList:
                currentSize += cnt.cnt_fullLength
                cnt.modified = False
            struct.pack_into(b"I", self._data, 4, currentSize)

    @property
    def pck_fullSize(self):
        return BYTES_LEN_MAGIC_HEADER + BYTES_LEN_PCK_SIZE_LEN + self.pck_payloadLen

    @property
    def pck_fullBinary(self):
        binary = MAGICBYTES + struct.pack("I", self.pck_payloadLen)
        for c in self.pck_cntList:
            binary += c.cnt_fullBinary
        return binary

    @property
    def pck_enumerateCnt(self):
        for pos, c in enumerate(self.pck_cntList):
            yield pos, c

    @property
    def pck_cntList(self):
        if not self.__cntList:
            self.__cntList = self.__parseAllCnt()
        return self.__cntList

    def __parseAllCnt(self):
        lst = []
        offset = self.cntOffset
        while offset < self.file.stat().st_size - 1:
            lst.append(self.__getCnt(offset))
            offset += BYTES_LEN_CNT_ID + BYTES_LEN_CNT_PAYLOAD_LEN + lst[-1].cnt_payloadLen
        return lst

    def __getCnt(self, offset):
        cntId = struct.unpack_from("H", self.readDataFromFile(offset, 2))[0]
        payloadLen = struct.unpack_from("I", self.readDataFromFile(offset + BYTES_LEN_CNT_ID, 4))[0]
        pktLen = BYTES_LEN_CNT_ID + BYTES_LEN_CNT_PAYLOAD_LEN + payloadLen

        data = self.readDataFromFile(offset, pktLen)
        if len(data) != pktLen:
            raise RuntimeError(f"File maybe corrupted. Please download again. File: {self.file.absolute()}")
        try:
            return CNT_HANDLER[cntId](data, offset)
        except KeyError:
            raise RuntimeError(f"failed with id: {cntId}\n"
                               f"New cnt id discovered in file: {self.file.absolute()}")
        # except TypeError:
        #     raise RuntimeError(f"failed with id: {cntId}\n{self.file.absolute()}")

    def _checkMagicBytes(self, errorMsg):
        if not self.pck_magicBytes == MAGICBYTES:
            raise RuntimeError(errorMsg)
