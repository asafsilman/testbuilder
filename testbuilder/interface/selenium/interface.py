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
import re
import time

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
        self.driver.maximize_window()

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
            for handle in self.driver.window_handles:
                try:
                    self.driver.switch_to.window(handle)
                    self.driver.close()
                except WebDriverException:
                    continue
            self.driver.quit()

    @action_word
    def CloseWindow(self, step_context):
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
        
        prefix,_,key = text.partition(".") # Map Special keys
        if prefix == "$Keys":
            text = getattr(keys.Keys, key)

        element.send_keys(text)

    @action_word
    def ClearField(self, step_context):
        """Clears the field of a selenium webelement

        Arguments:
            step_context {StepContext} -- The current step context
        """

        xpath = step_context.step_argument_1_mapped

        self.Exist(step_context)
        element = self.driver.find_element_by_xpath(xpath)
        element.clear()

    @action_word
    def Click(self, step_context):
        """Clicks a selenium webelement
        
        Arguments:
            step_context {StepContext} -- The current step context
        """

        xpath = step_context.step_argument_1_mapped

        self.Exist(step_context)
        
        for _ in range(self.retries): # Exist sometimes fails, retry to click element
            try:
                element = self.driver.find_element_by_xpath(xpath)
                element.click()
                break
            except WebDriverException:
                time.sleep(float(self.implicit_wait)/self.retries)
                continue
        else:
            raise Exception("Could not click on element")
        
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
            raise Exception("Element {0} not found".format(step_context.step_argument_1))

    @action_word
    def ExistFormatted(self, step_context):
        xpath = step_context.step_argument_1_mapped
        formatting = step_context.step_argument_2.split(';')

        step_context.step_argument_1_mapped = xpath.format(*formatting)

        self.Exist(step_context)

    @action_word
    def ClickFormatted(self, step_context):
        xpath = step_context.step_argument_1_mapped
        formatting = step_context.step_argument_2.split(';')

        step_context.step_argument_1_mapped = xpath.format(*formatting)

        self.Click(step_context)
        
    @action_word
    def SwitchFrame(self, step_context):
        xpath = step_context.step_argument_1_mapped

        frame = self.driver.find_element_by_xpath(xpath)

        self.driver.switch_to_default_content()
        self.driver.switch_to_frame(frame)
    
    @action_word
    def SwitchToDefaultFrame(self, step_context):
        self.driver.switch_to_default_content()

    @action_word
    def CheckExist(self, step_context):
        xpath = step_context.step_argument_1_mapped

        temp_wait = self.implicit_wait # Maintain this value
        
        self.set_implicit_wait(temp_wait/3)
        condition = all([
            self.wait_for_element_condition("element_to_be_clickable", xpath),
            self.wait_for_element_condition("visibility_of_element_located", xpath),
            self.wait_for_element_condition("presence_of_element_located", xpath)
        ])
        self.set_implicit_wait(temp_wait)

        step_context.step.result = condition

    @action_word
    def SwitchWindow(self, step_context):
        window_pattern = step_context.step_argument_1
        for _ in range(self.retries):
            for handle in self.driver.window_handles:
                try:
                    self.driver.switch_to.window(handle)
                    if re.match(window_pattern, self.driver.title):
                        return
                except WebDriverException:
                    continue
            time.sleep(self.implicit_wait)
        else:
            raise Exception(f"Could not switch to window with pattern {window_pattern}")
