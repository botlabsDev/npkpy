import hashlib
from pathlib import Path
from typing import List


def getAllNkpFiles(path, containStr=None):
    return path.glob(f"**/*{containStr}*.npk" if containStr else "**/*.npk")


def extractContainer(npkFile, exportFolder, filterContainer):
    for position, cnt in enumerate(npkFile.pck_cntList):
        if cnt.cnt_id in filterContainer:
            filePath = exportFolder / f"{position:03}_cnt_{cnt.cnt_idName}.raw"
            writeToFile(filePath, cnt.cnt_payload)


def writeToFile(file, payloads):
    written = 0
    if not isinstance(payloads, list):
        payloads = [payloads]

    with open(file, "wb") as f:
        for payload in payloads:
            f.write(payload)
            written += len(payload)


def getPktInfo(file):
    return [str(file.file.name)]


def getCntInfo(file) -> List:
    return [f"Cnt:{pos:3}:{c.cnt_idName}" for pos, c in file.pck_enumerateCnt]


def getFullPktInfo(file) -> List:
    output = getPktInfo(file)
    output += getCntInfo(file)
    for cnt in file.pck_cntList:
        output += getFullCntInfo(cnt)
    return output


def getFullCntInfo(cnt) -> List:
    info = []
    idName, options = cnt.output_cnt
    info.append(f"{idName}")
    for option in options:
        info.append(f"  {option}")
    return info


def sha1sumFromFile(file: Path):
    with file.open('rb') as f:
        return sha1sumFromBinary(f.read())


def sha1sumFromBinary(payloads):
    if len(payloads) == 0:
        return "<empty>"

    sha1 = hashlib.sha1()
    for payload in [payloads] if not isinstance(payloads, list) else payloads:
        sha1.update(payload)

    return sha1.digest()
