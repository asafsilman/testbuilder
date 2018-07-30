"""Basic action word interface"""

from testbuilder.core.base.baseinterface import TBBaseInterface, action_word
from testbuilder.core.exceptions import (ImproperlyConfigured, ActionWordException)
from testbuilder.core.base.basestep import StepStatus

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
            raise ActionWordException(f"Test does not have installed objectmap {object_map_name}")

        step_context.object_map = test.object_maps[object_map_name]
        step_context.object_map.switch_page(object_map_page)

    @action_word
    def If(self, step_context):
        arg1 = step_context.step_argument_1
        arg2 = step_context.step_argument_2

        if arg1 == arg2:
            return
        else:
            current_step = step_context.step
            next_step = self.find_matching_step(current_step, "If", "EndIf")
            self.mark_steps_as_skipped(current_step, next_step)

            step_context.next_step = next_step

    def mark_steps_as_skipped(self, start_step, last_step):
        current_step = start_step.next_step

        while current_step != last_step:
            current_step.status = StepStatus.SKIPPED
            current_step = current_step.next_step

    def find_matching_step(self, start_step, step_action, matching_step_action):
        current_step = start_step.next_step

        match_height = 0
        while current_step is not None:
            action = current_step.get_action()
            if action == step_action:
                match_height += 1
            if action == matching_step_action:
                if match_height == 0:
                    return current_step
                else:
                    match_height -= 1
            current_step = current_step.next_step
        raise ActionWordException(f"Could not find matching action word {matching_step_action}")

    @action_word
    def EndIf(self, step_context):
        pass

    @action_word
    def LaunchApp(self, step_context):
        pass