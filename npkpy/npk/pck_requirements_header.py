import struct
from npkpy.npk.cnt_basic import CntBasic, BYTES_LEN_CNT_PAYLOAD_LEN, BYTES_LEN_CNT_ID

NPK_REQUIREMENTS_HEADER = 3


class PckRequirementsHeader(CntBasic):
    def _version_one_and_two(self):
        def check(obj):
            if obj.cnt_structure_id > 0:
                return self(obj)
            return "<not available for version 0>"

        return check

    def _version_two_only(self):
        def check(obj):
            if obj.cnt_structure_id > 1:
                return self(obj)
            return "<not available for version 0,1>"

        return check

    def __init__(self, data, offset_in_pck):
        super().__init__(data, offset_in_pck)
        self._offset = offset_in_pck

    @property
    def _regular_cnt_id(self):
        return NPK_REQUIREMENTS_HEADER

    @property
    def cnt_structure_id(self) -> object:
        return struct.unpack_from(b"H", self._data, 6)[0]

    @property
    @_version_one_and_two
    def cnt_program_name(self):
        return bytes(struct.unpack_from(b"16B", self._data, 8)).decode().rstrip('\x00')

    @property
    @_version_one_and_two
    def cnt_os_version_min(self):
        revision = (struct.unpack_from(b"B", self._data, 24))[0]
        unknown_subrevision = (struct.unpack_from(b"B", self._data, 25))[0]
        minor = (struct.unpack_from(b"B", self._data, 26))[0]
        major = (struct.unpack_from(b"B", self._data, 27))[0]
        return f"{major}.{minor}.{revision} - rc(?): {unknown_subrevision}"

    @property
    @_version_one_and_two
    def cnt_null_block(self):
        return struct.unpack_from(b"BBBB", self._data, 28)

    @property
    @_version_one_and_two
    def cnt_os_version_max(self):
        revision = (struct.unpack_from(b"B", self._data, 32))[0]
        unknown_subrevision = (struct.unpack_from(b"B", self._data, 33))[0]
        minor = (struct.unpack_from(b"B", self._data, 34))[0]
        major = (struct.unpack_from(b"B", self._data, 35))[0]
        return f"{major}.{minor}.{revision} - rc(?): {unknown_subrevision}"

    @property
    @_version_two_only
    def cnt_flags(self):
        return struct.unpack_from(b"4B", self._data, 36)

    @property
    def cnt_full_binary(self):
        cnt_id = self.cnt_id
        payload_len = self.cnt_payload_len
        payload = struct.unpack_from(f"{self.cnt_payload_len}s", self._data,
                                     offset=BYTES_LEN_CNT_ID + BYTES_LEN_CNT_PAYLOAD_LEN)[0]
        return struct.pack("=HI", cnt_id, payload_len) + payload

    @property
    def output_cnt(self):
        _, opt = super().output_cnt
        options = [f"StructID:         {self.cnt_structure_id}",
                   f"Offset:           {self._offset}",
                   f"Program name:     {self.cnt_program_name}",
                   f"Null block:       {self.cnt_null_block}",
                   f"Os versionFrom:   {self.cnt_os_version_min}",
                   f"Os versionTo:     {self.cnt_os_version_max}",
                   f"Flags:            {self.cnt_flags}"
                   ]

        return f"{self.cnt_id_name}", opt + options
