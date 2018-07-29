import unittest
import os
from testbuilder.loader.excelloader.loader import ExcelTestLoader
from testbuilder.core.base.basefixtures import TBBaseFixture

class TestExcelLoader(unittest.TestCase):
    def setUp(self):
        self.testcase_path = os.path.join(
            os.path.dirname(__file__),
            "fixtures",
            "sample_testcase.xlsx"
        )
        self.loader = ExcelTestLoader()

    def test_load_tests(self):
        test = self.loader.load_tests(self.testcase_path)