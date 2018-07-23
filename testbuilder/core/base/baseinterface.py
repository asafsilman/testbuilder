"""Base Testbuilder Interface class"""
from testbuilder.conf import settings
from testbuilder.core.exceptions import ImproperlyConfigured
from testbuilder.core.base.basestep import StepStatus

def action_word(func):
    func.is_action_word=True
    return func

class TBBaseInterface:
    def dispatch(self, step_context):
        action = step_context.step_action
        defined_action_words = self.get_list_of_action_words()

        if action in defined_action_words:
            try:
                getattr(self, action)(step_context) # Run step
                self._pass_step(step_context) # Mark step as passed
            except Exception as e:
                self._fail_step(step_context, e) # Mark step as failed
        else:
            raise ImproperlyConfigured(f"Interface does not have a defined action {action}")

    def _pass_step(self, step_context):
        step_context.step.status = StepStatus.PASSED

    def _fail_step(self, step_context, e):
        step_context.step.status = StepStatus.FAILED

    def get_list_of_action_words(self):
        actions = []

        for item_name in dir(self):
            item = getattr(self, item_name, None)
            if callable(item):
                if getattr(item, "is_action_word", False) == True:
                    actions.append(item_name)

        return actions

    def ready(self):
        return True
