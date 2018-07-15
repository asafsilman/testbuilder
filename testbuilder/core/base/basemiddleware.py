"""Base Testbuilder Middleware class"""

class TBMiddleware:
    def process_step(self, step_context, test):
        """Overwrite this function by middleware class
        
        Arguments:
            step_context {StepContext} -- The step context
            test {TBBaseTest} -- The current test
        
        Returns:
            StepContext -- The step context
        """

        return step_context
