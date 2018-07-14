"""
Settings and configuration for Testbuider.

Values are read from module specified by the environment variable TESTBUILDER_SETTINGS_MODULE
then values are read from testbuilder.conf.global_settings.
"""
import importlib

from testbuilder.conf import global_settings

ENVIRONMENT_VARIBLE = "TESTBUILDER_SETTINGS_MODULE"