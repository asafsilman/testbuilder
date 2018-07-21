"""
Placeholder for future implementation
"""

from .load_tests import load_tests
from .load_engine import load_engine

import unittest

def run_test_case(file, file_type):
    engine = load_engine()

    # TODO
    # print(engine.interfaces)
    # print(engine.objectmap_parsers)
    # print(engine.middlewares)
    # print(engine.testloaders)
    # print(engine.profiles)

def run_unittests(verbose):
    package_tests = unittest.TestLoader().discover(start_dir="tests")

    verbosity=1
    if verbose:
        verbosity=2

    unittest.TextTestRunner(verbosity=verbosity).run(package_tests)