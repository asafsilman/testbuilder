"""Base Testbuilder test loader"""
from typing import List
from .basetest import TBBaseTest

class TBBaseTestLoader:
    def load_tests(self) -> List[TBBaseTest]:
        """Overwrite this function. Returns a list of tests.
        
        Returns:
            List[TBBaseTest] -- A list of test cases
        """
        
        raise NotImplementedError("Overwrite this function")
