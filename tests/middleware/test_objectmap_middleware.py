from testbuilder.objectmap.python.python_objectmap import PythonObjectMapParse
from testbuilder.middleware.objectmap.middleware import ObjectMapMiddleware
from testbuilder.core.base.basestep import (StepContext, TBBaseStep)
from testbuilder.core.base.basetest import TBBaseTest

import unittest

class TestObjectMapMiddleware(unittest.TestCase):
    def setUp(self):
        object_map_path = "testbuilder.objectmap.static.objectmap"
        parser = PythonObjectMapParse()

        object_map = parser.parse("test", object_map_path)
        object_map.switch_page("Sample")

        test = TBBaseTest()

        self.step_context = StepContext(test)
        self.step_context.object_map = object_map

        self.middleware = ObjectMapMiddleware()

    def test_middleware_before_step_one_argument(self):
        step = TBBaseStep(action="SampleAction", argument_1="sample_element")
        self.step_context.update_context(step, self.step_context)

        self.middleware.before_step(self.step_context)
        self.assertEqual(self.step_context.step_argument_1_mapped, "//sample")
        self.assertEqual(self.step_context.action_interface, "basic")

    def test_middleware_before_step_two_arguments(self):
        step = TBBaseStep(action="SampleAction", argument_1="sample_element", argument_2="sample_element_2")
        self.step_context.update_context(step, self.step_context)

        self.middleware.before_step(self.step_context)
        self.assertEqual(self.step_context.step_argument_1_mapped, "//sample")
        self.assertEqual(self.step_context.action_interface, "basic")

        self.assertEqual(self.step_context.step_argument_2_mapped, "//test/element")
