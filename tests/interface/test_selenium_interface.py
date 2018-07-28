from testbuilder.interface.selenium.interface import SeleniumInterface
from testbuilder.core.base.basetest import TBBaseTest
from testbuilder.core.base.basestep import (StepContext, TBBaseStep)

import unittest

@unittest.skip
class TestSeleniumInterface(unittest.TestCase):
    def setUp(self):
        self.interface = SeleniumInterface()

        test = TBBaseTest()
        self.step_context = StepContext(test)

    def test_LaunchDriver_Navigate_FireFox(self):
        step_1 = TBBaseStep(action="LaunchDriver", argument_1="FireFox")
        step_2 = TBBaseStep(action="Navigate", argument_1="http://www.google.com")

        self.step_context.update_context(step_1, self.step_context)

        self.interface.LaunchDriver(self.step_context)

        self.step_context.update_context(step_2, self.step_context)
        self.interface.Navigate(self.step_context)

    def test_LaunchDriver_Navigate_Chrome(self):
        step_1 = TBBaseStep(action="LaunchDriver", argument_1="Chrome")
        step_2 = TBBaseStep(action="Navigate", argument_1="http://www.google.com")

        self.step_context.update_context(step_1, self.step_context)

        self.interface.LaunchDriver(self.step_context)

        self.step_context.update_context(step_2, self.step_context)
        self.interface.Navigate(self.step_context)

    def tearDown(self):
        if self.interface.driver is not None:
            self.interface.driver.close()

@unittest.skip
class TestSeleniumInterfaceChrome(unittest.TestCase):
    def setUp(self):
        self.interface = SeleniumInterface()

        test = TBBaseTest()
        step_1 = TBBaseStep(action="LaunchDriver", argument_1="Chrome")
        self.step_context = StepContext(test)

        self.step_context.update_context(step_1, self.step_context)
        self.interface.LaunchDriver(self.step_context)

    def test_Type(self):
        step_1 = TBBaseStep(action="Navigate", argument_1="http://www.google.com")
        self.step_context.update_context(step_1, self.step_context)

        self.interface.Navigate(self.step_context)


        step_2 = TBBaseStep(action="Type", argument_2="Testing Search")
        self.step_context.update_context(step_2, self.step_context)
        self.step_context.step_argument_1_mapped = "//input[@name='q']"

        self.interface.Type(self.step_context)

    def test_Click(self):
        step_1 = TBBaseStep(action="Navigate", argument_1="http://www.google.com")
        self.step_context.update_context(step_1, self.step_context)

        self.interface.Navigate(self.step_context)


        step_2 = TBBaseStep(action="Click", argument_1="Search")
        self.step_context.update_context(step_2, self.step_context)
        self.step_context.step_argument_1_mapped = "//input[@name='btnK']"

        self.interface.Click(self.step_context)

    def test_Exist(self):
        step_1 = TBBaseStep(action="Navigate", argument_1="http://www.google.com")
        self.step_context.update_context(step_1, self.step_context)
        self.interface.Navigate(self.step_context)

        step_2 = TBBaseStep(action="Click", argument_1="Search")
        self.step_context.update_context(step_2, self.step_context)
        self.step_context.step_argument_1_mapped = "//input[@name='btnK']"

        self.interface.Exist(self.step_context)

    def test_Exist_fail(self):
        step_1 = TBBaseStep(action="Navigate", argument_1="http://maxdesign.com.au/jobs/sample-accessibility/05-forms/attribute-disabled.html")
        self.step_context.update_context(step_1, self.step_context)
        self.interface.Navigate(self.step_context)

        step_2 = TBBaseStep(action="Click", argument_1="Search")
        self.step_context.update_context(step_2, self.step_context)
        self.step_context.step_argument_1_mapped = "//button[@text()='five']"

        # Speed up test a bit
        self.interface.set_implicit_wait(0.1)

        with self.assertRaises(Exception):
            self.interface.Exist(self.step_context)

    def test_search_google(self):
        step_1 = TBBaseStep(action="Navigate", argument_1="http://www.google.com")
        self.step_context.update_context(step_1, self.step_context)
        self.interface.Navigate(self.step_context)

        step_2 = TBBaseStep(action="Type", argument_2="Testing Search")
        self.step_context.update_context(step_2, self.step_context)
        self.step_context.step_argument_1_mapped = "//input[@name='q']"
        self.interface.Type(self.step_context)

        step_3 = TBBaseStep(action="Click", argument_1="Search")
        self.step_context.update_context(step_3, self.step_context)
        self.step_context.step_argument_1_mapped = "//input[@name='btnK']"

        self.interface.Click(self.step_context)

        self.assertIn("Testing Search", self.interface.driver.title)

    def tearDown(self):
        if self.interface.driver is not None:
            self.interface.driver.close()
