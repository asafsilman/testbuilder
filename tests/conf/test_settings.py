import unittest
import os

from testbuilder.conf.settings import Settings

class TestSettings(unittest.TestCase):
    def setUp(self):
        # TEST_VALUE = 5
        sample_settings_file = "tests.conf.sample_settings"
        
        self.prev_settings_module = os.environ.get("TESTBUILDER_SETTINGS_MODULE")
        os.environ.setdefault("TESTBUILDER_SETTINGS_MODULE", sample_settings_file)

    def test_settings(self):
        settings = Settings()
        self.assertEqual(settings.TEST_VALUE, 5, "Failed to load setting module")
        
    def tearDown(self):
        os.environ.setdefault("TESTBUILDER_SETTINGS_MODULE", self.prev_settings_module)
