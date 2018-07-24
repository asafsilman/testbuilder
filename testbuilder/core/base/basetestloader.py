"""Base Testbuilder test loader"""
from typing import List
from .basetest import TBBaseTest

class TBBaseTestLoader:
    def load_tests(self, test_location) -> List[TBBaseTest]:
        """Overwrite this function. Returns a testscase.
        
        Returns:
            TBBaseTest -- loaded testcase
        """
        
        raise NotImplementedError("Overwrite this function")
