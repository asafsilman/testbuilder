"""Load Testcase from YAML file"""

import os
import re
from typing import List

import yaml

from testbuilder.conf import settings
from testbuilder.core.base.basetest import TBBaseTest
from testbuilder.core.base.basetestloader import TBBaseTestLoader
from testbuilder.core.exceptions import ImproperlyConfigured

from .yamlstep import YAMLStep


class YAMLTestLoader(TBBaseTestLoader):
    tests = []

    def load_tests(self) -> List[TBBaseTest]:
        return self.tests

    def add_test(self, path) -> None:
        """Parse and add a test to tests
        
        Arguments:
            path {str} -- The path to the yaml test case
        """
        if not os.path.exists(path):
            raise ImproperlyConfigured(f"Path does not exist: {path}")

        yaml_test_data = None
        with open(path) as f:
            yaml_test_data = yaml.load(f)

        # Check that test steps exists
        test_steps = yaml_test_data.get("steps")
        if not test_steps:
            raise ImproperlyConfigured("Testcase has no steps, stopping")

        # Create base test with properties
        test_properties = yaml_test_data.get("properties", {}) # Load property mapping, or empty dict type
        test = TBBaseTest(**test_properties) # load all properties to test

        # Load all additional properties to testcase
        test_additional_properties = yaml_test_data.get("additional_properties")
        if test_additional_properties: 
            for setting in test_additional_properties: # Add all settings to testcase
                value = test_additional_properties[setting]
                test.load_additional_property(setting, value)

        # Load test fixtures

        first_step = None
        _cur_step = None

        # Load test steps
        for i, step in enumerate(test_steps):
            if i == 0: # First step
                first_step = self.load_test_step(step, test)
                _cur_step = first_step
                continue
            next_step = self.load_test_step(step, test) # Load the next step
            _cur_step.add_next_step(next_step) # Register the next step
            _cur_step = next_step # Replace current step with next step

        test.load_steps(first_step)

        self.tests.append(test)

    def load_test_step(self, step, test) -> YAMLStep:
        """Loads a test step
        
        Arguments:
            step {dict} -- Step details from file
        
        Returns:
            YAMLStep -- The loaded step
        """

        step_mapping = {
            "action": self.get_step_field(step.get("action"), test),
            "argument_1": self.get_step_field(step.get("argument_1"), test),
            "argument_2": self.get_step_field(step.get("argument_2"), test),
            "tag": self.get_step_field(step.get("tag"), test)
        }

        step = YAMLStep(**step_mapping)

        return step

    def get_step_field(self, field, test):
        if field is None:
            return ""
        elif re.match(r"^\$settings\.", field, flags=re.IGNORECASE):
            return self._step_field_from_settings(field)
        elif re.match(r"^\$fixtures\.", field, flags=re.IGNORECASE):
            return field # TODO: Value form fixtures
        elif re.match(r"^\$steps\.", field, flags=re.IGNORECASE):
            return field # TODO: Value from steps result
        else:
            return field

    def _step_field_from_settings(self, field):
        """Gets a value that is stored in settings

        `field` is in the format '$settings.<setting>(.subsetting)*'
        
        Arguments:
            field {str} -- The setting field to fetch
        """

        split = field.split(".")[1:] # ignore first item which is '$setting'
        
        if len(split) == 1:
            s = split[0]
            return settings[s]
        else:
            s0 = split[0]
            curr_s = settings[s0]
            for s in split[1:]:
                curr_s = curr_s[s]
            return curr_s

    
