"""Load Testcase from YAML file"""

import os
import re

import yaml

from testbuilder.conf import settings
from testbuilder.core.base.basetest import TBBaseTest
from testbuilder.core.base.basetestloader import TBBaseTestLoader
from testbuilder.core.exceptions import ImproperlyConfigured
from testbuilder.fixture.csv_fixture import CSVFixture

from .yamlstep import YAMLStep


class YAMLTestLoader(TBBaseTestLoader):

    def load_test(self, test_location) -> TBBaseTest:
        """Parse and add a test to tests
        
        Arguments:
            path {str} -- The path to the yaml test case
        """
        if not os.path.exists(test_location):
            raise ImproperlyConfigured(f"Path does not exist: {test_location}")

        yaml_test_data = None
        with open(test_location) as f:
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
        test_fixtures = yaml_test_data.get("fixtures")
        if test_fixtures:
            for fixture_name in test_fixtures: # Iterate over each fixture in testcase
                fixture_path = test_fixtures[fixture_name]
                
                if not os.path.exists(fixture_path): #If fixture is relative path
                    fixture_path = os.path.join(
                        os.path.dirname(test_location), # Testcase path
                        fixture_path # Fixture path relative to testcase
                    )
                fixture = CSVFixture(fixture_name, fixture_path) # Create fixutre
                
                test.load_fixtures(fixture) # Load fixture in test

        first_step = None
        _cur_step = None

        # Load test steps
        for i, step in enumerate(test_steps):
            if i == 0: # First step
                first_step = self.load_test_step(step, test)
                _cur_step = first_step
                continue
            next_step = self.load_test_step(step, test, first_step) # Load the next step
            _cur_step.add_next_step(next_step) # Register the next step
            _cur_step = next_step # Replace current step with next step

        test.load_steps(first_step)

        return test

    def load_test_step(self, step, test, first_step=None) -> YAMLStep:
        """Loads a test step
        
        Arguments:
            step {dict} -- Step details from file

        Keyword Arguments:
            first_step {TBBaseStep} -- First Step (default: {None})

        Returns:
            YAMLStep -- The loaded step
        """

        step_mapping = {
            "action": self.get_step_field(step.get("action"), test, first_step),
            "argument_1": self.get_step_field(step.get("argument_1"), test, first_step),
            "argument_2": self.get_step_field(step.get("argument_2"), test, first_step),
            "tag": self.get_step_field(step.get("tag"), test, first_step)
        }

        step = YAMLStep(**step_mapping)

        return step

    def get_step_field(self, field, test, first_step):
        if field is None:
            return ""
        elif re.match(r"^\$settings\.", field, flags=re.IGNORECASE):
            return self._step_field_from_settings(field)
        elif re.match(r"^\$fixtures\.", field, flags=re.IGNORECASE):
            return self._step_field_from_fixture(field, test)
        elif re.match(r"^\$steps\.", field, flags=re.IGNORECASE):
            return self._step_field_from_step(field, first_step)
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

    def _step_field_from_fixture(self, field, test):
        _,_,fixture_info = field.partition(".")

        f0 = fixture_info.find('[')

        fixture_name = fixture_info[0:f0]
        fixture_column = fixture_info[f0+2:-2]

        fixture = test.fixtures.get(fixture_name)

        if fixture is None:
            raise ImproperlyConfigured(f"Test does not contain fixture{fixture_name}")

        return lambda: fixture.get_value(test.get_current_iteration(), fixture_column)

    def _step_field_from_step(self, field, first_step):
        _,_,step_info = field.partition(".")
        
        filterby,_,value = step_info.partition('=')

        filterby = filterby.lower()
        value = value[1:-1]

        if filterby=="tag":
            return self._get_step_result_by_tag(first_step, value)

    def _get_step_result_by_tag(self, first_step, tag):
        current_step = first_step
        while True:
            tag_value = getattr(current_step, "tag", None)
            if tag_value == tag:
                return lambda: current_step.get_result()

            if current_step.is_last_step():
                break
            current_step = current_step.next_step
        raise ImproperlyConfigured(f"No step found with tag {tag}")