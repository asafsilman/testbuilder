"""Base test class"""
import importlib

from testbuilder.core.exceptions import (
    StepException
)
from testbuilder.core.base.basestep import TBBaseStep

class TBBaseTest:
    """
    TestBuilder Base Test

    A TBBaseTest is container for a single testcase.
    
    A TBBaseTest is responsible for maintaing
    
    * Steps within a testcase
    * Maintaing the current step of the testcase
    * Determine the next step in the testcase
    * Step Middlewares
    * Results Middlewares
    """

    test_name=""

    first_step=None
    current_step=None

    step_middlewares = [] # an ordered collection of middlewares
    results_middlewares = [] # an ordered collection of middlewares

    def __init__(self, *args, **kwargs):
        self.test_name = kwargs.get("test_name", "")

    def load_steps(self, first_step):
        """Loads the first step for the test.
        
        Arguments:
            first_step {TBBaseStep} -- The first step in the testcase
        
        Raises:
            TypeError -- Raised if `first_step is not of type TBBaseStep`
            StepException -- Raised if the step isn't the first step
        """

        if not isinstance(first_step, TBBaseStep):
            raise TypeError("excpected 'first_step' to by of type TBBaseStep")
        if not first_step.is_first_step():
            raise StepException("This is not the first step of the test")
        self.first_step = first_step
        self.current_step = self.first_step

    def load_step_interface(self, interface_name):
        pass

    
            