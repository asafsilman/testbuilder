"""Base Testbuilder Middleware class"""

class TBBaseMiddleware:
    def before_step(self, step_context) -> None:
        """Overwrite this function by middleware class
        
        Arguments:
            step_context {StepContext} -- The step context
        """
        pass

    def after_step(self, step_context) -> None:
        """Overwrite this function by middleware class
        
        Arguments:
            step_context {StepContext} -- The step context
        """
        pass

    def step_failure(self, step_context) -> None:
        """Overwrite thir function by middleware class
        
        Arguments:
            step_context {StepContext} -- The step context
        """
        pass

    def tear_down_before_step(self, step_context) -> None:
        pass

    def tear_down_after_step(self, step_context) -> None:
        pass

    def ready(self):
        return True
