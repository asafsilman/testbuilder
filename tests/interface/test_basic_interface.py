from testbuilder.interface.basic.interface import BasicInterface
from testbuilder.core.base.basetest import TBBaseTest
from testbuilder.core.base.basestep import (StepContext, TBBaseStep, StepStatus)
from testbuilder.core.base.baseobjectmap import (TBBaseObjectMap, TBBasePage)

import unittest

class TestBasicInterface(unittest.TestCase):
    def setUp(self):
        self.test = TBBaseTest()
        self.interface = BasicInterface()

    def test_object_map(self):
        # Prepare objectmap
        object_map = TBBaseObjectMap("test_object_map")
        page1 = TBBasePage("test_page", {"obj": "sample:test"})
        object_map.load_page(page1)

        # Prepare step context
        s_c = StepContext(self.test)
        s_c.step_argument_1 = "test_object_map"
        s_c.step_argument_2 = "test_page"

        self.test.load_object_map(object_map, "test_object_map")

        self.interface.ObjectMap(s_c)

        self.assertIsNotNone(s_c.object_map)
        self.assertEqual(s_c.object_map, object_map)
        self.assertEqual(s_c.object_map.get_current_page(), page1)

    def test_if_equal(self):
        step_1 = TBBaseStep(action="If", argument_1="A", argument_2="A")
        step_2 = TBBaseStep(action="")
        step_3 = TBBaseStep(action="EndIf")

        step_1.add_next_step(step_2)
        step_2.add_next_step(step_3)

        s_c = StepContext(self.test)
        s_c.update_context(step_1, s_c)

        self.interface.If(s_c)
        self.assertEqual(s_c.next_step, step_2)

    def test_if_not_equal(self):
        step_1 = TBBaseStep(action="If", argument_1="A", argument_2="B")
        step_2 = TBBaseStep(action="")
        step_3 = TBBaseStep(action="EndIf")

        step_1.add_next_step(step_2)
        step_2.add_next_step(step_3)

        s_c = StepContext(self.test)
        s_c.update_context(step_1, s_c)

        self.interface.If(s_c)
        self.assertEqual(step_2.status, StepStatus.SKIPPED)

        self.assertNotEqual(step_3.status, StepStatus.SKIPPED)
        self.assertEqual(s_c.next_step, step_3)

    def test_nested_if_not_equal(self):
        step_1 = TBBaseStep(action="If", argument_1="A", argument_2="B")
        step_2 = TBBaseStep(action="If", argument_1="A", argument_2="A")
        step_3 = TBBaseStep(action="")
        step_4 = TBBaseStep(action="EndIf") # Skip this EndIf
        step_5 = TBBaseStep(action="EndIf") # Close on this EndIf

        step_1.add_next_step(step_2)
        step_2.add_next_step(step_3)
        step_3.add_next_step(step_4)
        step_4.add_next_step(step_5)

        s_c = StepContext(self.test)
        s_c.update_context(step_1, s_c)

        self.interface.If(s_c)
        self.assertEqual(step_2.status, StepStatus.SKIPPED)
        self.assertEqual(step_3.status, StepStatus.SKIPPED)
        self.assertEqual(step_4.status, StepStatus.SKIPPED)

        self.assertNotEqual(step_5.status, StepStatus.SKIPPED)
        self.assertEqual(s_c.next_step, step_5)
