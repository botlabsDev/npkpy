import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

from pytest_httpserver import HTTPServer
from urlpath import URL

from tools.download_all_packages import fetchWebsite, extractDownloadLinks, filterLinks, \
    unpackFile


class Test_MikroTikDownloader(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        print("setup Class!")
        cls.s = HTTPServer()
        cls.s.start()
        cls.testUrl = f"http://localhost:{cls.s.port}"

        # cls.s.expect_request("/download/archive").respond_with_data(createArchiveWebsite(cls.testUrl))
        # cls.s.expect_request("/routeros/6.36.4/all_packages-mipsbe-6.36.4.zip").respond_with_data(b"data",

    #                                                                                              content_type="application/zip")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.s.stop()

    def setUp(self) -> None:
        self.s.clear()

    def test_downloadWebsite(self):
        self.s.expect_request("/").respond_with_data(b"testData")

        result = fetchWebsite(f"http://localhost:{self.s.port}")

        self.assertEqual("testData", result)

    def test_extractDownloadLinks(self):
        testData = "dummyTest \n"
        testData += "<td><a href=\"//filterString.com/prod/vers/programA-arch-version.zip\">program-arch-version.zip>\n"
        testData += "dummyTest \n"

        result = extractDownloadLinks(testData, "filterString.com")

        self.assertEqual([URL("//filterString.com/prod/vers/programA-arch-version.zip")], list(result))

    def test_filterForSpecificLinks_basedOnSuffix(self):
        links = [URL("//filterString.com/prod/vers/programA-arch-version.zip"),
                 URL("//filterString.com/prod/vers/programB-arch-version.WRONGSUFFIX")]

        result = filterLinks(links, [("program", ".zip")])

        self.assertEqual([URL("//filterString.com/prod/vers/programA-arch-version.zip")], list(result))

    def test_filterForSpecificLinks_basedOnProgram(self):
        links = [URL("//filterString.com/prod/vers/programA-arch-version.exe"),
                 URL("//filterString.com/prod/vers/programB-arch-version.zip")]

        result = filterLinks(links, ([("programB", ".zip")]))

        self.assertEqual([URL("//filterString.com/prod/vers/programB-arch-version.zip")], list(result))

    def test_dontExtractZip_fileDontExist(self):
        file = Path(tempfile.NamedTemporaryFile(suffix="WRONGSUFFIX").name)

        unpackFile(file)

    def test_dontExtractZip_fileHasNoZipSuffix(self):
        file = Path(tempfile.NamedTemporaryFile(suffix="WRONGSUFFIX").name)
        file.touch()

        unpackFile(file)

    def test_extractZip_validatePayload(self):
        zipFile, origTxtFile = _createTxtInZipFile(txtPayload="TEST DATA")
        unzipedFile = Path(f"{origTxtFile.parent}/{origTxtFile.absolute()}")

        unpackFile(zipFile)

        self.assertTrue(zipFile.exists())
        self.assertTrue(unzipedFile.exists())
        self.assertEqual("TEST DATA", unzipedFile.read_text())


def _createTxtInZipFile(txtPayload):
    txtFile = Path(tempfile.NamedTemporaryFile(suffix=".txt").name)
    zipFile = Path(tempfile.NamedTemporaryFile(suffix=".zip").name)
    with txtFile.open("w") as f:
        f.write(txtPayload)
    with ZipFile(zipFile, 'w') as zipObj:
        zipObj.write(txtFile.absolute())
    return zipFile, txtFile


def createArchiveWebsite(testUrl):
    return f"""
           <tr>
           <td width='40px'><div class='icon zip'></div></td>
           <td><a href=\"//{testUrl}/routeros/6.36.4/all_packages-mipsbe-6.36.4.zip\">all_packages-mipsbe-6.36.4>
           <td class='pl'>mipsbe</td>
           </tr>
            """
