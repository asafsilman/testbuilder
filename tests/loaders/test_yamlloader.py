import unittest
import os
from testbuilder.loaders.yamlloader.loader import YAMLTestLoader
from testbuilder.core.base.basefixtures import TBBaseFixture

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

        self.assertEqual(len(self.loader.load_tests()), 1)
        test = self.loader.load_tests()[0]

        self.assertEqual(test.test_name, 'sample_testcase')
        self.assertEqual(test.test_iterations, 1)
        
        self.assertIsInstance(test.fixtures['umrns'], TBBaseFixture)
        self.assertTrue(test.first_step.is_first_step())
