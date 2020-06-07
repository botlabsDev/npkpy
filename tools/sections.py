from collections import Counter
from pathlib import Path
from typing import Tuple

from more_itertools import peekable


def getBinaryFromFile(file: Path):
    with file.open("rb") as f:
        data = f.read()
        for d in data:
            yield d

def findDiffs(lastFile, file):
    bLastFile = peekable(getBinaryFromFile(lastFile))
    bfile = peekable(getBinaryFromFile(file))

    sections = []
    counter = -1
    hasChanged = (bLastFile.peek() == bfile.peek())
    sectionTracker = dict({True: 0, False: 0})

    while True:
        try:
            while (next(bLastFile) == next(bfile)) is hasChanged:
                counter += 1
        except StopIteration:
            sections.append((max(sectionTracker.values()), counter, not hasChanged))
            break

        sectionTracker[hasChanged] = counter + 1
        hasChanged = not hasChanged
        sections.append((sectionTracker[hasChanged], counter, hasChanged))
        counter += 1

    return sections


def findSections(filesDict: dict) -> Tuple[str, Counter]:
    cTotal = Counter()
    for (program, versionFiles) in filesDict.items():
        lastFile = None
        c = Counter()
        for (version, file) in versionFiles.items():
            if lastFile is not None:
                diffs = findDiffs(lastFile.file, file.file)
                c.update(diffs)
                cTotal.update(diffs)
            lastFile = file
        yield program, c
    yield "__total", cTotal
