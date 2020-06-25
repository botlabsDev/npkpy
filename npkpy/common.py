import hashlib
from pathlib import Path
from typing import List


def get_all_nkp_files(path, contain_str=None):
    return path.glob(f"**/*{contain_str}*.npk" if contain_str else "**/*.npk")


def extract_container(npk_file, export_folder, container_ids):
    for position, cnt in enumerate(npk_file.pck_cnt_list):
        if cnt.cnt_id in container_ids:
            file_path = export_folder / f"{position:03}_cnt_{cnt.cnt_id_name}.raw"
            write_to_file(file_path, cnt.cnt_payload)


def write_to_file(file, payloads):
    payloads = [payloads] if not isinstance(payloads, list) else payloads
    with open(file, "wb") as _file:
        for payload in payloads:
            _file.write(payload)


def get_short_pkt_info(file) -> List:
    return [str(file.file.name)]


def get_full_pkt_info(file) -> List:
    output = get_short_pkt_info(file)
    output += get_short_cnt_info(file)
    for cnt in file.pck_cnt_list:
        output += get_full_cnt_info(cnt)
    return output


def get_short_cnt_info(file) -> List:
    return [f"Cnt:{pos:3}:{c.cnt_id_name}" for pos, c in file.pck_enumerate_cnt]


def get_full_cnt_info(cnt) -> List:
    info = []
    id_name, options = cnt.output_cnt
    info.append(f"{id_name}")
    for option in options:
        info.append(f"  {option}")
    return info


def sha1_sum_from_file(file: Path):
    with file.open('rb') as _file:
        return sha1_sum_from_binary(_file.read())


def sha1_sum_from_binary(payloads):
    if len(payloads) == 0:
        return b"<empty>"

    sha1 = hashlib.sha1()
    for payload in [payloads] if not isinstance(payloads, list) else payloads:
        sha1.update(payload)

    return sha1.digest()


class NPKIdError(BaseException):
    pass


class NPKMagicBytesError(BaseException):
    pass


class NPKError(BaseException):
    pass
