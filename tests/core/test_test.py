import unittest
from testbuilder.core.base.test import TBBaseTest
from testbuilder.core.base.step import TBBaseStep

from testbuilder.core.exceptions import StepException

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
    
    def test_add_step_wrong(self):
        with self.assertRaises(StepException):
            self.test.load_steps(self.step_2)
