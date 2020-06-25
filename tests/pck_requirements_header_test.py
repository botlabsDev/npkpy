import unittest

from npkpy.npk.pck_requirements_header import PckRequirementsHeader
from tests.constants import get_dummy_requirements_header


class Test_pktRequirementsHeader(unittest.TestCase):
    def setUp(self) -> None:
        self.cnt = createRequirementsHeaderCnt(structId=0)

    def test_validateCntId(self):
        self.assertEqual(3, self.cnt.cnt_id)

    def test_getCntStructId(self):
        self.assertEqual(0, createRequirementsHeaderCnt(structId=0).cnt_structure_id)
        self.assertEqual(1, createRequirementsHeaderCnt(structId=1).cnt_structure_id)
        self.assertEqual(2, createRequirementsHeaderCnt(structId=2).cnt_structure_id)


class Test_pktRequirementsHeader_StructIdZero(unittest.TestCase):
    def setUp(self) -> None:
        self.cnt = createRequirementsHeaderCnt(structId=0)

    def test_getCntFlags(self):
        self.assertEqual("<not available for version 0,1>", self.cnt.cnt_flags)

    def test_getProgramName_NotAvailableForVersionZero(self):
        self.assertEqual("<not available for version 0>", self.cnt.cnt_program_name)

    def test_getOsVersionMin_NotAvailableForVersionZero(self):
        self.assertEqual("<not available for version 0>", self.cnt.cnt_os_version_min)

    def test_getNullBlock_NotAvailableForVersionZero(self):
        self.assertEqual("<not available for version 0>", self.cnt.cnt_null_block)

    def test_getOsVersionMax_NotAvailableForVersionZero(self):
        self.assertEqual("<not available for version 0>", self.cnt.cnt_os_version_max)

    def test_getFlags_NotAvailableForVersionZero(self):
        self.assertEqual("<not available for version 0,1>", self.cnt.cnt_flags)

    def test_FullBinary(self):
        self.assertEqual(get_dummy_requirements_header(structId=0), self.cnt.cnt_full_binary)

    def test_getOutput(self):
        self.assertEqual(('PckRequirementsHeader',
                          ['Cnt id:           3',
                           'Cnt offset:       0',
                           'Cnt len:          41',
                           'Payload len:      35',
                           "Payload[0:10]:    b'\\x00\\x00abcdefgh' [...] ",
                           'StructID:         0',
                           'Offset:           0',
                           'Program name:     <not available for version 0>',
                           'Null block:       <not available for version 0>',
                           'Os versionFrom:   <not available for version 0>',
                           'Os versionTo:     <not available for version 0>',
                           'Flags:            <not available for version 0,1>']), self.cnt.output_cnt)


class Test_pktRequirementsHeader_StructIdOne(unittest.TestCase):
    def setUp(self) -> None:
        self.cnt = createRequirementsHeaderCnt(structId=1)

    def test_getProgramName(self):
        self.assertEqual("abcdefghijklmnop", self.cnt.cnt_program_name)

    def test_getOsVersionMin(self):
        self.assertEqual("1.2.3 - rc(?): 4", self.cnt.cnt_os_version_min)

    def test_getNullBlock(self):
        self.assertEqual((0, 0, 0, 0), self.cnt.cnt_null_block)

    def test_getOsVersionMax(self):
        self.assertEqual("5.6.7 - rc(?): 8", self.cnt.cnt_os_version_max)

    def test_getFlags(self):
        self.assertEqual("<not available for version 0,1>", self.cnt.cnt_flags)

    def test_FullBinary(self):
        self.assertEqual(get_dummy_requirements_header(structId=1), self.cnt.cnt_full_binary)

    def test_getOutput(self):
        self.assertEqual(('PckRequirementsHeader',
                          ['Cnt id:           3',
                           'Cnt offset:       0',
                           'Cnt len:          41',
                           'Payload len:      35',
                           "Payload[0:10]:    b'\\x01\\x00abcdefgh' [...] ",
                           'StructID:         1',
                           'Offset:           0',
                           'Program name:     abcdefghijklmnop',
                           'Null block:       (0, 0, 0, 0)',
                           'Os versionFrom:   1.2.3 - rc(?): 4',
                           'Os versionTo:     5.6.7 - rc(?): 8',
                           'Flags:            <not available for version 0,1>']), self.cnt.output_cnt)


class Test_pktRequirementsHeader_StructIdTwo(unittest.TestCase):
    def setUp(self) -> None:
        self.cnt = createRequirementsHeaderCnt(structId=2)

    def test_getProgramName(self):
        self.assertEqual("abcdefghijklmnop", self.cnt.cnt_program_name)

    def test_getOsVersionMin(self):
        self.assertEqual("1.2.3 - rc(?): 4", self.cnt.cnt_os_version_min)

    def test_getNullBlock(self):
        self.assertEqual((0, 0, 0, 0), self.cnt.cnt_null_block)

    def test_getOsVersionMax(self):
        self.assertEqual("5.6.7 - rc(?): 8", self.cnt.cnt_os_version_max)

    def test_getFlags(self):
        self.assertEqual((0, 0, 0, 0), self.cnt.cnt_flags)

    def test_FullBinary(self):
        self.assertEqual(get_dummy_requirements_header(structId=2), self.cnt.cnt_full_binary)

    def test_getOutput(self):
        self.assertEqual(('PckRequirementsHeader',
                          ['Cnt id:           3',
                           'Cnt offset:       0',
                           'Cnt len:          41',
                           'Payload len:      35',
                           "Payload[0:10]:    b'\\x02\\x00abcdefgh' [...] ",
                           'StructID:         2',
                           'Offset:           0',
                           'Program name:     abcdefghijklmnop',
                           'Null block:       (0, 0, 0, 0)',
                           'Os versionFrom:   1.2.3 - rc(?): 4',
                           'Os versionTo:     5.6.7 - rc(?): 8',
                           'Flags:            (0, 0, 0, 0)']), self.cnt.output_cnt)


def createRequirementsHeaderCnt(structId):
    return PckRequirementsHeader(get_dummy_requirements_header(structId), offset_in_pck=0)
