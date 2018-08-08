import unittest
from testbuilder.core.base.basetest import TBBaseTest
from testbuilder.core.base.basestep import TBBaseStep, StepContext
from testbuilder.core.base.baseobjectmap import TBBaseObjectMap
from testbuilder.core.base.basemiddleware import TBBaseMiddleware

from testbuilder.core.exceptions import StepException, ImproperlyConfigured
from testbuilder.interface.basic.interface import BasicInterface
from testbuilder.middleware.basic.middleware import BasicMiddleware

from testbuilder.core.base.basetest import (
    MIDDLEWARE_MODE_AFTER_STEP,
    MIDDLEWARE_MODE_BEFORE_STEP,
    MIDDLEWARE_MODE_STEP_FAILURE,
    MIDDLEWARE_MODE_TEARDOWN_AFTER_STEP,
    MIDDLEWARE_MODE_TEARDOWN_BEFORE_STEP
)

class SampleMiddleware(TBBaseMiddleware):
    def after_step(self, step_context):
        step_context.additional_settings["MiddlewareRun"] = "after_step"

    def before_step(self, step_context):
        step_context.additional_settings["MiddlewareRun"] = "before_step"
    
    def step_failure(self, step_context):
        step_context.additional_settings["MiddlewareRun"] = "step_failure"

    def tear_down_after_step(self, step_context):
        step_context.additional_settings["MiddlewareRun"] = "tear_down_after_step"

    def tear_down_before_step(self, step_context):
        step_context.additional_settings["MiddlewareRun"] = "tear_down_before_step"

class TestTBBaseTest(unittest.TestCase):
    def setUp(self):
        self.step_1 = TBBaseStep()
        self.step_2 = TBBaseStep()
        self.step_3 = TBBaseStep()

        self.step_1.add_next_step(self.step_2)
        self.step_2.add_next_step(self.step_3)

        self.test = TBBaseTest()

    def test_add_step(self):
        self.test.load_steps(self.step_1)

        self.assertEqual(self.test.first_step, self.step_1, "First step is not loaded")
        self.assertEqual(self.test.current_step, self.step_1, "Current step is not loaded")

    def test_add_tear_down_steps(self):
        self.test.load_tear_down_steps(self.step_1)

        self.assertEqual(self.test.tear_down_first_step, self.step_1, "First step is not loaded")
    
    def test_add_step_wrong(self):
        with self.assertRaises(StepException):
            self.test.load_steps(self.step_2)

    def test_ready(self):
        self.test.run_test=True
        self.assertFalse(self.test.ready())

        self.test.load_interface(BasicInterface, "basic")
        self.assertFalse(self.test.ready())

        self.test.load_middleware(BasicMiddleware)
        self.assertFalse(self.test.ready())

        self.test.load_steps(self.step_1)
        self.assertTrue(self.test.ready())

    def test_load_interface(self):
        self.test.load_interface(BasicInterface, "basic")

        with self.assertRaises(ImproperlyConfigured):
            # Try to load middleware as interface
            self.test.load_interface(BasicMiddleware, "basic_failure")

    def test_load_middleware(self):
        self.test.load_middleware(BasicMiddleware)

        with self.assertRaises(ImproperlyConfigured):
            # Try to load interface as middleware
            self.test.load_middleware(BasicInterface)

    def test_load_objectmap(self):
        object_map = TBBaseObjectMap("objectmap")

        self.test.load_object_map(object_map, "objectmap")

        with self.assertRaises(ImproperlyConfigured):
            # Try load middleware as objectmap
            self.test.load_object_map(BasicMiddleware(), "objectmap")

    def test_run_middlewares(self):
        def create_new_context():
            c_x = StepContext(self.test)
            c_x.additional_settings["MiddlewareRun"] = None
            return c_x
        
        self.test.load_middleware(SampleMiddleware)
        
        step_context = create_new_context()
        self.test.run_middlewares(step_context, MIDDLEWARE_MODE_AFTER_STEP)
        self.assertEqual(step_context.additional_settings["MiddlewareRun"], "after_step")

        step_context = create_new_context()
        self.test.run_middlewares(step_context, MIDDLEWARE_MODE_BEFORE_STEP)
        self.assertEqual(step_context.additional_settings["MiddlewareRun"], "before_step")

        step_context = create_new_context()
        self.test.run_middlewares(step_context, MIDDLEWARE_MODE_STEP_FAILURE)
        self.assertEqual(step_context.additional_settings["MiddlewareRun"], "step_failure")
        
        step_context = create_new_context()
        self.test.run_middlewares(step_context, MIDDLEWARE_MODE_TEARDOWN_AFTER_STEP)
        self.assertEqual(step_context.additional_settings["MiddlewareRun"], "tear_down_after_step")

        step_context = create_new_context()
        self.test.run_middlewares(step_context, MIDDLEWARE_MODE_TEARDOWN_BEFORE_STEP)
        self.assertEqual(step_context.additional_settings["MiddlewareRun"], "tear_down_before_step")
        