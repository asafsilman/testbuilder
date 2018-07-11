"""Base step class"""

class BaseStepAttributeProxy:
    def resolve_attribute(self):
        """Overwrite this function.
        Implement this function for resolve attribute at runtime
        
        Raises:
            NotImplementedError -- Raised if this function is not implemented yet
        """

        raise NotImplementedError 

def check_attribute_for_init(attribute):
    if isinstance(attribute, BaseStepAttributeProxy):
        return attribute
    raise TypeError("Attribute is expected to be of type 'BaseStepAttributeProxy'")


class BaseStep:
    """
    A step is an extension of a doubly linked list.

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

    def __init__(self, *args, **kwargs):
        self.action = check_attribute_for_init(kwargs.get("action"))
        self.argument_1 = check_attribute_for_init(kwargs.get("argument_1"))
        self.argument_2 = check_attribute_for_init(kwargs.get("argument_2"))

    def add_next_step(self, next_step):
        """Adds next step for current step.
        Also adds a backreference in next step to current step
        
        Arguments:
            next_step {BaseStep} -- The next step
        
        Raises:
            TypeError -- This is raised if step is not of type BaseStep
        """

        if not isinstance(next_step, BaseStep):
            raise TypeError("Expected step to be of type 'BaseStep'")
        self.next_step = next_step
        next_step.previous_step = self # Add back reference to step

    def is_last_step(self):
        """Returns whether there is a step following current step
        
        Returns:
            Boolean -- Is this the last step
        """

        return self.next_step is None

    def is_first_step(self):
        """Returns whether there is a step preceding current step
        
        Returns:
            Boolean -- Is this the first step
        """

        return self.previous_step is None

    def get_action(self):
        """Loads the `action` attribute for the current step
        
        Returns:
            Any -- Resolved attribute
        """

        return self.action.resolve_attribute()

    def get_argument_1(self):
        """Loads the `argument_1` attribute for the current step
        
        Returns:
            Any -- Resolved attribute
        """
        return self.argument_1.resolve_attribute()

    def get_argument_2(self):
        """Loads the `argument_2` attribute for the current step
        
        Returns:
            Any -- Resolved attribute
        """
        return self.argument_2.resolve_attribute()
