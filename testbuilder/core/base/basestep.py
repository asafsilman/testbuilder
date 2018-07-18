"""Base step class"""
from __future__ import annotations

from enum import Enum

class StepStatus(Enum):
    PASSED = 1
    FAILED = 2
    NOT_STARTED = 3
    IN_PROGRESS = 4

class StepContext:
    step_action = None
    step_argument_1 = None
    step_argument_2 = None

    next_step = None

    def __init__(self, step):
        if not isinstance(step, TBBaseStep):
            raise TypeError("Step must be of type TBBaseStep")
        self.step = step

    def get_next_step(self) -> TBBaseStep:
        """Returns the next step in test
        
        Returns:
            TBBaseStep -- The next step in test
        """

        if self.next_step is not None:
            return self.next_step
        else:
            return self.step.next_step

class TBBaseStep:
    """
    TestBuilder Base Step

    A TBBaseStep is an extension of a doubly linked list.

    Each step has a reference to the next step -> `next_step`
    In addition to a reference to the previous step -> `previous_step`

    If `next_step` is None, then its the last step
    If `previous_step` is None, then its the first step
    """

    next_step=None
    previous_step=None

    action=None
    argument_1=None
    argument_2=None
    result=None

    status=StepStatus.NOT_STARTED

    def __init__(self, *args, **kwargs):
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
