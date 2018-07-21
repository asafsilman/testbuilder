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

    def ready(self):
        return True
