"""
Settings and configuration for Testbuider.

Values are read from module specified by the environment variable TESTBUILDER_SETTINGS_MODULE
then values are read from testbuilder.conf.global_settings.
"""
import importlib
import os

from testbuilder.conf import global_settings
from testbuilder.core.exceptions import ImproperlyConfigured

ENVIRONMENT_VARIBLE = "TESTBUILDER_SETTINGS_MODULE"

class Settings:
    def __init__(self):
        # Load default settings
        for setting in dir(global_settings):
            if setting.isupper():
                setattr(self, setting, getattr(global_settings, setting))

        self.settings_module = os.environ.get(ENVIRONMENT_VARIBLE)
        if self.settings_module is not None:
            self._setup()


    def _setup(self):
        """
        Load settings from module specifiec in ENVIRONMENT_VARIABLE
        """

        mod = importlib.import_module(self.settings_module)
        for setting in dir(mod):
            if setting.isupper():
                setting_value = getattr(mod, setting)
                setattr(self, setting, setting_value)

    def __getitem__(self, name):
        return getattr(self, name)

    def __setitem__(self, name, value):
        return setattr(self, name, value)
