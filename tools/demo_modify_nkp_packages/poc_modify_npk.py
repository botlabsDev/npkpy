from pathlib import Path
from pprint import pprint

from npkpy.npk.npk import Npk


## KEEP IN MIND: MODIFICATIONS WILL INVALIDATE THE NPK PACKAGE SIGNATURE!
##               THE ROUTER WON'T INSTALL THE PACKAGE.


def modify_poc():
    npk_file = Npk(Path("tests/testData/6_48_4/gps-6.48.4.npk"))

    # print overview
    print("----Overview--------------------")
    pprint([f"pos: {pos:2} - Name: {cnt.cnt_id_name} (id:{cnt.cnt_id:2})" for pos, cnt in npk_file.pck_enumerate_cnt])
    print("-------------------------------")

    # The following code example will modify the payload section of PckDescription
    CNT_ID = 4  # PckDescription

    print("Payload original:")
    print_overview(npk_file, cnt_id=CNT_ID)

    print("overwrite payload - same size:")
    npk_file.pck_cnt_list[CNT_ID].cnt_payload = b"a" * 25
    print_overview(npk_file, cnt_id=CNT_ID)

    # Modifying the size of the payload can affect the whole npk package and
    # forces recalculations in other containers of this package
    print("Payload new - small size:")
    npk_file.pck_cnt_list[CNT_ID].cnt_payload = b"b" * 10
    print_overview(npk_file, cnt_id=CNT_ID)

    print("Payload new - increased:")
    npk_file.pck_cnt_list[CNT_ID].cnt_payload = b"c" * 100
    print_overview(npk_file, cnt_id=CNT_ID)

    print("Write File: modified.npk")
    Path("modified.npk").write_bytes(npk_file.pck_full_binary)

    # Parse the new npk file as shown blow:
    # $ npkpy --files modified.npk --show-container


def print_overview(npk_file, cnt_id):
    cnt = npk_file.pck_cnt_list[cnt_id]
    print("Cnt payload:      ", cnt.cnt_payload)
    print("Cnt payload len:  ", cnt.cnt_payload_len)
    print("Cnt len:          ", cnt.cnt_full_length)
    print("pkg len:          ", npk_file.pck_payload_len)
    print("-------------------------------")


if __name__ == '__main__':
    modify_poc()
