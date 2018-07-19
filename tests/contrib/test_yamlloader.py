import unittest
import os
from testbuilder.loaders.yamlloader.loader import YAMLTestLoader

class TestYAMLTestLoader(unittest.TestCase):
    def setUp(self):
        self.testcase_path = os.path.join(
            os.path.dirname(__file__),
            "fixtures",
            "sample_testcase.yaml"
        )
        self.loader = YAMLTestLoader()

    def test_add_test(self):
        self.loader.add_test(self.testcase_path)
        
