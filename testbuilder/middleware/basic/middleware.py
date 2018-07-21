from testbuilder.core.base.basemiddleware import TBBaseMiddleware

class BasicMiddleware(TBBaseMiddleware):
    def before_step(self, step_context):
        pass

    def after_step(self, step_context):
        pass