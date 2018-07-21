"""Base Testbuilder Middleware class"""
from .basestep import StepContext

class TBBaseMiddleware:
    def process_step(self, step_context, test) -> StepContext:
        """Overwrite this function by middleware class
        
        Arguments:
            step_context {StepContext} -- The step context
            test {TBBaseTest} -- The current test
        
        Returns:
            StepContext -- The step context
        """
        raise NotImplementedError("Overwrite this function")
