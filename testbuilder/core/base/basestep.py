"""Base step class"""
from __future__ import annotations

from enum import Enum

class StepStatus(Enum):
    PASSED = 1
    FAILED = 2
    NOT_STARTED = 3
    IN_PROGRESS = 4
    SKIPPED = 5

class StepContext:
    def __init__(self, test):
        from .basetest import TBBaseTest

        if not isinstance(test, TBBaseTest):
            raise TypeError("test must be of type TBBaseTest")
        self.object_map = None
        self.test = test

        self.additional_settings = {}
        self.step_number = 0

    def update_context(self, step, previous_context):
        if not isinstance(step, TBBaseStep):
            raise TypeError("step must be of type TBBaseStep")

        self.object_map = previous_context.object_map
        self.test = previous_context.test

        self.step = step

        self.additional_settings = previous_context.additional_settings
        self.step_number = previous_context.step_number+1

        self.action_interface = None

        self.step_action = step.get_action()
        self.step_argument_1 = step.get_argument_1()
        self.step_argument_2 = step.get_argument_2()

        self.next_step = step.next_step

class TBBaseStep:
    """
    TestBuilder Base Step

    A TBBaseStep is an extension of a doubly linked list.

    Each step has a reference to the next step -> `next_step`
    In addition to a reference to the previous step -> `previous_step`

    If `next_step` is None, then its the last step
    If `previous_step` is None, then its the first step
    """

    def __init__(self, *args, **kwargs):
        self.next_step=None
        self.previous_step=None
        self.status=StepStatus.NOT_STARTED

        self.result=None

        self.action = kwargs.get("action")
        self.argument_1 = kwargs.get("argument_1")
        self.argument_2 = kwargs.get("argument_2")

    def add_next_step(self, next_step) -> TBBaseStep:
        """Adds next step for current step.
        Also adds a backreference in next step to current step
        
        Arguments:
            next_step {TBBaseStep} -- The next step
        
        Raises:
            TypeError -- This is raised if step is not of type TBBaseStep
        """

        if not isinstance(next_step, TBBaseStep):
            raise TypeError("Expected step to be of type 'TBBaseStep'")
        self.next_step = next_step
        next_step.previous_step = self # Add back reference to step

    def is_last_step(self) -> bool:
        """Returns whether there is a step following current step
        
        Returns:
            Boolean -- Is this the last step
        """

        return self.next_step is None

    def is_first_step(self) -> bool:
        """Returns whether there is a step preceding current step
        
        Returns:
            Boolean -- Is this the first step
        """

        return self.previous_step is None

    def get_action(self):
        if callable(self.action):
            return self.action()
        return self.action

    def get_argument_1(self):
        if callable(self.argument_1):
            return self.argument_1() #pylint: disable=E1102
        return self.argument_1

    def get_argument_2(self):
        if callable(self.argument_2):
            return self.argument_2() #pylint: disable=E1102
        return self.argument_2

    def get_result(self):
        if callable(self.result):
            return self.result() #pylint: disable=E1102
        return self.result
