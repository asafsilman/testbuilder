"""Base Testbuilder Interface class"""
from testbuilder.conf import settings

def action_word(func):
    func.is_action_word=True
    return func

class TBBaseInterface:
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
