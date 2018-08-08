import unittest
from testbuilder.core.base.basetest import TBBaseTest
from testbuilder.core.base.basestep import TBBaseStep, StepContext
from testbuilder.core.base.baseobjectmap import TBBaseObjectMap
from testbuilder.core.base.basemiddleware import TBBaseMiddleware
from testbuilder.core.base.baseinterface import TBBaseInterface, action_word

from testbuilder.core.exceptions import StepException, ImproperlyConfigured

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

class SampleInterface(TBBaseInterface):
    @action_word
    def SampleAction(self, step_context):
        return

    @action_word
    def FailAction(self, step_context):
        raise Exception()

class TestTBBaseTest(unittest.TestCase):
    def setUp(self):
        self.step_1 = TBBaseStep()
        self.step_2 = TBBaseStep()

        self.step_1.add_next_step(self.step_2)

        self.test = TBBaseTest()

    def test_add_step(self):
        self.test.load_steps(self.step_1)

        self.assertEqual(self.test.first_step, self.step_1, "First step is not loaded")
        self.assertEqual(self.test.current_step, self.step_1, "Current step is not loaded")
    
    def test_get_current_iteration(self):
        self.assertEqual(self.test.get_current_iteration(), 0)

    def test_configure_next_iteration(self):
        self.test.load_steps(self.step_1)
        self.assertEqual(self.test.get_current_iteration(), 0)
        
        self.test.current_step = self.step_2
        self.test.configure_next_iteration()

        self.assertEqual(self.test.get_current_iteration(), 1)
        self.assertEqual(self.test.current_step, self.step_1)

    def test_add_step_wrong(self):
        with self.assertRaises(StepException):
            self.test.load_steps(self.step_2)

        with self.assertRaises(TypeError):
            self.test.load_steps(None)

    def test_add_tear_down_steps(self):
        self.test.load_tear_down_steps(self.step_1)

        self.assertEqual(self.test.tear_down_first_step, self.step_1, "First step is not loaded")

    def test_add_tear_down_steps_wrong(self):
        with self.assertRaises(StepException):
            self.test.load_tear_down_steps(self.step_2)

        with self.assertRaises(TypeError):
            self.test.load_tear_down_steps(None)

    def test_ready(self):
        self.assertFalse(self.test.ready())

        self.test.run_test=True
        self.assertFalse(self.test.ready())

        self.test.load_interface(SampleInterface, "basic")
        self.assertFalse(self.test.ready())

        self.test.load_middleware(SampleMiddleware)
        self.assertFalse(self.test.ready())

        self.test.load_steps(self.step_1)
        self.assertTrue(self.test.ready())

    def test_load_interface(self):
        self.test.load_interface(SampleInterface, "basic")

        with self.assertRaises(ImproperlyConfigured):
            # Try to load middleware as interface
            self.test.load_interface(SampleMiddleware, "basic_failure")

    def test_load_middleware(self):
        self.test.load_middleware(SampleMiddleware)

        with self.assertRaises(ImproperlyConfigured):
            # Try to load interface as middleware
            self.test.load_middleware(SampleInterface)

    def test_load_objectmap(self):
        object_map = TBBaseObjectMap("objectmap")

        self.test.load_object_map(object_map, "objectmap")

        with self.assertRaises(ImproperlyConfigured):
            # Try load middleware as objectmap
            self.test.load_object_map(SampleMiddleware(), "objectmap")

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
        
    def test_execute_step(self):
        self.test.load_interface(SampleInterface, "sample")

        step_1 = TBBaseStep(action="SampleAction")
        step_2 = TBBaseStep(action="SampleActionFail")

        step_1.add_next_step(step_2)

        c_x = StepContext(self.test); c_x.update_context(step_1, c_x)
        self.test.execute_step(c_x) # No interface defined

        c_x = StepContext(self.test); c_x.update_context(step_1, c_x)
        c_x.action_interface = "sample"
        self.test.execute_step(c_x) # Interface defined

        # Interface defined, but not installed
        with self.assertRaises(ImproperlyConfigured):
            c_x = StepContext(self.test); c_x.update_context(step_1, c_x)
            c_x.action_interface = "sample_fail"
            self.test.execute_step(c_x)

        # Action not defined
        with self.assertRaises(ImproperlyConfigured):
            c_x = StepContext(self.test); c_x.update_context(step_2, c_x)
            self.test.execute_step(c_x)

    def test_run(self):
        step_1 = TBBaseStep(action="SampleAction")
        step_2 = TBBaseStep(action="SampleAction")
        step_1.add_next_step(step_2)

        self.test.run_test=True
        self.test.load_interface(SampleInterface, "basic")
        self.test.load_middleware(SampleMiddleware)
        self.test.load_steps(step_1)
        self.test.load_tear_down_steps(step_1)

        self.test.run()

    def test_run_fail(self):
        with self.assertRaises(ImproperlyConfigured):
            self.test.run()
        
        step_1 = TBBaseStep(action="SampleAction")
        step_2 = TBBaseStep(action="FailAction")
        step_1.add_next_step(step_2)

        self.test.run_test=True
        self.test.load_interface(SampleInterface, "basic")
        self.test.load_middleware(SampleMiddleware)
        self.test.load_steps(step_1)

        self.test.run()
