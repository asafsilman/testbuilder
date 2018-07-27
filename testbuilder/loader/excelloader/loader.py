"""Load Testcase from Excel file"""

import os

from testbuilder.conf import settings
from testbuilder.core.base.basetest import TBBaseTest
from testbuilder.core.base.basetestloader import TBBaseTestLoader
from testbuilder.core.exceptions import ImproperlyConfigured

from typing import List

class ExcelTestLoader(TBBaseTestLoader):
    def load_tests(self, test_location) -> List[TBBaseTest]:
        """Parse and add a test to tests
        
        Arguments:
            path {str} -- The path to the excel test case
        """
        if not os.path.exists(test_location):
            raise ImproperlyConfigured(f"Path does not exist: {test_location}")
