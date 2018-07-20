from testbuilder.core.base.basestep import TBBaseStep

class YAMLStep(TBBaseStep):
    tag = ""

    def __init__(self, *args, **kwargs):
        self.tag = kwargs.get("tag", "")
        super().__init__(*args, **kwargs)
