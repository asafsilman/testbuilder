"""Load Testcase from Excel file"""

from .util import colnum_string, colstring_num, split_cell_string

import os

from testbuilder.conf import settings
from testbuilder.core.base.basetest import TBBaseTest
from testbuilder.core.base.basetestloader import TBBaseTestLoader
from testbuilder.core.exceptions import ImproperlyConfigured

from typing import List

import xlwings as xw
import pandas as pd

class ExcelTestLoader(TBBaseTestLoader):
    def load_tests(self, test_location) -> List[TBBaseTest]:
        """Parse and add a test to tests
        
        Arguments:
            path {str} -- The path to the excel test case
        """
        if not os.path.exists(test_location):
            raise ImproperlyConfigured(f"Path does not exist: {test_location}")

        wb = xw.Book(test_location) # Workbook
        dash =  wb.sheets[settings["DASHBOARD_SHEET_NAME"]] # Dashboard worksheet

        test_environment = dash.range(settings["EXCEL_ENVIRONMENT"]).value

        table = dash.range(settings["TEST_TABLE_START"])\
            .options(pd.DataFrame, expand="table", index=False).value

        tests = []

        (_, start_row) = split_cell_string(settings["TEST_TABLE_START"])

        for test in table.iterrows():
            print(colnum_string(table.columns.get_loc("Run")+1))
            print(test[1]["Run"])
