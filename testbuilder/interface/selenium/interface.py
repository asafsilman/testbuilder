"""Selenium Interface for interacting with web applications"""

from testbuilder.core.base.baseinterface import TBBaseInterface, action_word
from testbuilder.conf import settings

from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.common.exceptions import WebDriverException

import os

class SeleniumInterface(TBBaseInterface):
    def __init__(self):
        self.driver=None # The webdriver instance
        self.driver_base_path = settings["SELENIUM_DRIVER_BASE_PATH"]
        self.implicit_wait = settings["SELENIUM_IMPLICIT_WAIT"] or 0

        self.retries = settings["SELENIUM_RETRY_ATTEMPTS"]

    @action_word
    def LaunchDriver(self, step_context):
        """Launches a selenium webdriver
        
        Arguments:
            step_context {StepContext} -- The current step context
        """
        
        driver_type = step_context.step_argument_1 or ""
     
        if driver_type.lower()=="chrome":
            self._launch_chrome()
        elif driver_type.lower()=="edge":
            raise NotImplementedError("Edge Broweser is not implemented yet")
        elif driver_type.lower()=="firefox":
            self._launch_firefox()
        elif driver_type.lower() in ['internet explorer', 'ie']:
            raise NotImplementedError("IE Broweser is not implemented yet")
        else:
            self._launch_chrome()

        self.set_implicit_wait(self.implicit_wait)

    def _launch_chrome(self):
        driver_executable = settings["SELENIUM_CHROME_DRIVER"]
        driver_version = settings["SELENIUM_CHROME_VERSION"]
        driver_path = os.path.join(self.driver_base_path, driver_executable)

        options = webdriver.ChromeOptions()

        if driver_version[0] == 2:
            options.add_experimental_option("useAutomationExtension", False)

        self.driver = webdriver.Chrome(executable_path=driver_path, options=options)

    def _launch_firefox(self):
        driver_executable = settings["SELENIUM_FIREFOX_DRIVER"]
        driver_path = os.path.join(self.driver_base_path, driver_executable)

        self.driver = webdriver.Firefox(executable_path=driver_path)

    def set_implicit_wait(self, wait):
        self.implicit_wait = wait
        self.driver.implicitly_wait(wait)

    @action_word
    def CloseDriver(self, step_context):
        if self.driver is not None:
            self.driver.close()

    @action_word
    def Navigate(self, step_context):
        """Navigates the selenium webdriver to a webpage
        
        Arguments:
            step_context {StepContext} -- The current step context
        """
        page = step_context.step_argument_1

        self.driver.get(page)

    @action_word
    def Type(self, step_context):
        """Types some text to a selenium webelement

        Arguments:
            step_context {StepContext} -- The current step context
        """

        xpath = step_context.step_argument_1_mapped
        text = str(step_context.step_argument_2)

        self.Exist(step_context)
        element = self.driver.find_element_by_xpath(xpath)
        element.send_keys(text)

    @action_word
    def Click(self, step_context):
        """Clicks a selenium webelement
        
        Arguments:
            step_context {StepContext} -- The current step context
        """

        xpath = step_context.step_argument_1_mapped

        self.Exist(step_context)
        element = self.driver.find_element_by_xpath(xpath)
        element.click()
        
    def wait_for_element_condition(self, condition, xpath, timeout=None):
        if timeout is None: timeout = self.implicit_wait
        
        search_by_method = getattr(By, "XPATH")
        search_condition = getattr(EC, condition)
        driver_wait_until = WebDriverWait(self.driver, timeout).until
        try:
            # Raises timout exception if not found
            driver_wait_until(search_condition((search_by_method, xpath)))
            return True
        except WebDriverException:
            return False

    @action_word
    def Exist(self, step_context):
        xpath = step_context.step_argument_1_mapped

        for _ in range(self.retries):
            condition = all([
                self.wait_for_element_condition("element_to_be_clickable", xpath),
                self.wait_for_element_condition("visibility_of_element_located", xpath),
                self.wait_for_element_condition("presence_of_element_located", xpath)
            ])
            if condition is True:
                break
        else: # If all iterations passed, but still no element
            raise Exception("Element {0} not found")
        