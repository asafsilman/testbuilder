"""Objectmap middleware for loading"""

from testbuilder.core.base.basemiddleware import TBBaseMiddleware
from testbuilder.core.exceptions import ObjectMapException

class ObjectMapMiddleware(TBBaseMiddleware):
    def before_step(self, step_context):
        if step_context.object_map is None:
            return

        # Map argument 1
        try:
            arg1 = step_context.step_argument_1
            step_context.step_argument_1_mapped = step_context.object_map.get_element(arg1)
        except ObjectMapException:
            return

        # Map argument 2
        try:
            arg2 = step_context.step_argument_2
            step_context.step_argument_2_mapped = step_context.object_map.get_element(arg2)
        except ObjectMapException:
            return
