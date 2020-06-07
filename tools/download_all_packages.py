import socket
import sys
import urllib.request
import zipfile
from datetime import datetime
from pathlib import Path
from time import sleep
from urllib.error import HTTPError, URLError
from zipfile import ZipFile

from urlpath import URL


class MikroTikDownloader:

    def __init__(self, dstPath):

        self.dstPath = Path(dstPath)
        self.sleepTime = 1
        socket.setdefaulttimeout(10)

    def downloadAll(self, urls):
        missingFiles = self._determineMissingFiles(urls)
        for link in missingFiles:
            unpackFile(self._downloadFile(link))

    def _downloadFile(self, url):
        def _progress(count, block_size, total_size):
            progress = (float(count * block_size) / float(total_size) * 100.0)
            if int(progress) > 100:
                raise RuntimeError("AccessDenied")
            sys.stderr.write(self._msg(url) + ': [%.1f%%] ' % progress)
            sys.stderr.flush()

        targetFile = self._convertToLocalFilePath(url)
        targetFile.parent.mkdir(exist_ok=True, parents=True)

        while True:
            try:
                urllib.request.urlretrieve(f"http:{url.resolve()}", targetFile, _progress)
                self.msg(url, "[100.0%]")
                self.dec_sleep()
                break
            except HTTPError as e:
                self.msg(url, f"[failed] (Error code: {e.code})")
                break
            except socket.timeout:
                self.msg(url, "[failed] (Timeout)")
                self.inc_sleep()
            except RuntimeError as e:
                self.msg(url, f"[failed] ([{e}])")
                if targetFile.exists():
                    targetFile.unlink()
                break
            except URLError as e:
                self.msg(url, f"[failed] (Error code: {e})")
                self.inc_sleep()

        return targetFile

    def inc_sleep(self):
        sleep(self.sleepTime)
        self.sleepTime += 1

    def dec_sleep(self):
        if self.sleepTime > 1:
            self.sleepTime -= 1

    def _determineMissingFiles(self, urls):
        for url in urls:
            if not self._convertToLocalFilePath(url).exists():
                yield url
            else:
                self.msg(url, "[ok]")

    def msg(self, url, msg):
        print(f"{self._msg(url)}: {msg}")

    def _msg(self, url):
        return f"\r[{datetime.now().time()}] Download {url.name:35}"

    def _convertToLocalFilePath(self, link: URL):
        pktName = arc = version = ""
        elements = link.stem.split("-")
        count = len(elements)
        if count == 2:
            pktName, version = elements
        if count == 3:
            pktName, arc, version = elements
        return self.dstPath / pktName / arc / version / link.name


def fetchWebsite(url):
    with urllib.request.urlopen(url) as response:
        return response.read().decode("utf-8")


def extractDownloadLinks(tHtml, filterString):
    return (URL(line.split('"')[1]) for line in tHtml.split() if filterString in line)


def filterLinks(tLinks, filters):
    return (link for link in tLinks if
            any(True for name, suffix in filters
                if name in link.stem and
                suffix in link.suffix
                )
            )


def unpackFile(file: Path):
    if file.exists() and file.suffix == ".zip":
        try:
            with ZipFile(file, 'r') as zipObj:
                zipObj.extractall(file.parent)
        except zipfile.BadZipFile:
            file.unlink()


if __name__ == "__main__":
    html = fetchWebsite("https://mikrotik.com/download/archive")
    links = extractDownloadLinks(html, "download.mikrotik.com")
    selectedLinks = filterLinks(links, [("all_packages", ".zip"),
                                        (".", ".npk")
                                        ]
                                )
    mtd = MikroTikDownloader("./downloads")
    mtd.downloadAll(selectedLinks)
