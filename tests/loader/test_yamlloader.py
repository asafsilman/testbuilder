import unittest
import os
from testbuilder.loader.yamlloader.loader import YAMLTestLoader
from testbuilder.core.base.basefixtures import TBBaseFixture

class TestYAMLTestLoader(unittest.TestCase):
    def setUp(self):
        self.testcase_path = os.path.join(
            os.path.dirname(__file__),
            "fixtures",
            "sample_testcase.yaml"
        )
        self.loader = YAMLTestLoader()

    def test_load_tests(self):
        test = self.loader.load_tests(self.testcase_path)[0]

        self.assertEqual(test.test_name, 'sample_testcase')
        self.assertEqual(test.test_iterations, 1)
        self.assertTrue(test.run_test)

        self.assertIsInstance(test.fixtures['umrns'], TBBaseFixture)
        self.assertTrue(test.first_step.is_first_step())
