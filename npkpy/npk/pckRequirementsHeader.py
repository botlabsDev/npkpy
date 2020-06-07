import struct
from npkpy.npk.cntBasic import NpkContainerBasic

NPK_REQUIREMENTS_HEADER = 3


class PckRequirementsHeader(NpkContainerBasic):
    def _versionOneTwo(foo):
        def check(self):
            if self.cnt_structure_id > 0:
                return foo(self)
            return "<not available for version 0>"

        return check

    def _versionTwo(foo):
        def check(self):
            if self.cnt_structure_id > 1:
                return foo(self)
            return "<not available for version 0,1>"

        return check

    def __init__(self, data, offsetInPck):
        super().__init__(data, offsetInPck)
        self._offset = offsetInPck

    @property
    def _regularCntId(self):
        return NPK_REQUIREMENTS_HEADER

    @property
    def cnt_structure_id(self):
        return struct.unpack_from(b"H", self._data, 6)[0]

    @property
    @_versionOneTwo
    def cnt_programName(self):
        return bytes(struct.unpack_from(b"16B", self._data, 8)).decode().rstrip('\x00')

    @property
    @_versionOneTwo
    def cnt_osVersionFrom(self):
        revision = (struct.unpack_from(b"B", self._data, 24))[0]
        rc = (struct.unpack_from(b"B", self._data, 25))[0]
        minor = (struct.unpack_from(b"B", self._data, 26))[0]
        major = (struct.unpack_from(b"B", self._data, 27))[0]
        return f"{major}.{minor}.{revision} - rc(?): {rc}"

    @property
    @_versionOneTwo
    def cnt_nullBlock(self):
        return struct.unpack_from(b"BBBB", self._data, 28)

    @property
    @_versionOneTwo
    def cnt_osVersionTo(self):
        revision = (struct.unpack_from(b"B", self._data, 32))[0]
        rc = (struct.unpack_from(b"B", self._data, 33))[0]
        minor = (struct.unpack_from(b"B", self._data, 34))[0]
        major = (struct.unpack_from(b"B", self._data, 35))[0]
        return f"{major}.{minor}.{revision} - rc(?): {rc}"

    @property
    @_versionTwo
    def cnt_flags(self):
        return struct.unpack_from(b"4B", self._data, 36)

    @property
    def cnt_fullBinary(self):
        id = self.cnt_id
        payload_len = self.cnt_payloadLen
        payload = struct.unpack_from(f"{self.cnt_payloadLen}s", self._data, 2 + 4)[0]

        # if self.cnt_structure_id > 2:
        #      print(self.cnt_flags)
        #      return struct.pack(f"HH", id, payload_len) + se + payload
        return struct.pack(f"=HI", id, payload_len) + payload

    @property
    def output_cnt(self):
        idName, opt = super().output_cnt
        options = [f"Cnt id:           {self.cnt_id}",
                   f"StructID:         {self.cnt_structure_id}",
                   f"Offset:           {self._offset}",
                   f"Program name:     {self.cnt_programName}",
                   f"Null block:       {self.cnt_nullBlock}",
                   f"Os versionFrom:   {self.cnt_osVersionFrom}",
                   f"Os versionTo:     {self.cnt_osVersionTo}",
                   f"Flags:            {self.cnt_flags}"
                   ]

        return (f"{self.cnt_idName}", opt + options)
