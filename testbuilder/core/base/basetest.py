"""Base test class"""
import importlib

from testbuilder.core.exceptions import (
    StepException
)
from testbuilder.core.base.basestep import TBBaseStep, StepContext

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

    middlewares = [] # an ordered collection of middlewares
    interfaces = {}

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

    def load_step_middleware(self, module_name):
        mod = importlib.import_module(module_name)

        self.middlewares.append(mod)

    def ready(self):
        """Checks the tests is ready to start execution

        * Checks first_step is loaded
        * Checks middlewares are not empty
        * Checks interfaces are not empty
        
        Returns:
            [type] -- [description]
        """

        return False

    
            