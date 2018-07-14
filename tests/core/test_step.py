import unittest
from testbuilder.core.base.step import TBBaseStep

class TestTBBaseStep(unittest.TestCase):

    def setUp(self):
        self.step_1 = TBBaseStep()
        self.step_2 = TBBaseStep()
        self.step_3 = TBBaseStep()

    def test_add_next_step(self):
        self.step_1.add_next_step(self.step_2)
        self.step_2.add_next_step(self.step_3)

        self.assertEqual(self.step_1.next_step, self.step_2, "Step 2 does not follow step 1")
        self.assertEqual(self.step_2.next_step, self.step_3, "Step 3 does not follow step 2")
    
    def test_add_next_step_wrong(self):
        with self.assertRaises(TypeError):
            self.step_1.add_next_step("Incorrect data")

    def test_is_last_step(self):
        self.step_1.add_next_step(self.step_2)
        self.assertTrue(self.step_2.is_last_step, "Expected this step to be the last step")

    def test_is_first_step(self):
        self.step_1.add_next_step(self.step_2)
        self.assertTrue(self.step_1.is_first_step, "Expected this step to be the first step")
