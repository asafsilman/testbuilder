"""Basic action word interface"""


from testbuilder.core.base.baseinterface import TBBaseInterface, action_word
from testbuilder.core.exceptions import ImproperlyConfigured

import os

class BasicInterface(TBBaseInterface):
    @action_word
    def ObjectMap(self, step_context):
        """
        Changes the current object map for the test
        Updates the objectmap page
        
        Arguments:
            step_context {StepContext} -- Current step context
        """

        test = step_context.test

        object_map_name = step_context.step_argument_1
        object_map_page = step_context.step_argument_2

        if object_map_name not in test.object_maps:
            raise ImproperlyConfigured(f"Test does not have installed objectmap {object_map_name}")

        step_context.object_map = test.object_maps[object_map_name]
        step_context.object_map.switch_page(object_map_page)

    @action_word
    def LaunchApp(self, step_context):
        pass