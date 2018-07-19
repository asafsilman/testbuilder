from testbuilder.core.base.basestep import TBBaseStep

class YAMLStep(TBBaseStep):
    tag = ""

    def __init__(self, *args, **kwargs):
        self.tag = kwargs.get("tag", "")
        super().__init__(*args, **kwargs)

    def get_action(self):
        if callable(self.action):
            return self.action()
        else: return self.action

    def get_argument_1(self):
        if callable(self.argument_1):
            return self.argument_1()
        return self.argument_1

    def get_argument_2(self):
        if callable(self.argument_2):
            return self.argument_2()
        return self.argument_2