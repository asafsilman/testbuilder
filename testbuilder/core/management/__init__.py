"""
Placeholder for future implementation
"""

from .load_engine import load_engine

import unittest

def run_test_case(file, file_type, profile):
    engine = load_engine()

    tests = engine.create_tests(file, file_type, profile)

    for test in tests:
        print(test.run_test)
        if test.run_test:
            test.run()

def run_unittests(verbose):
    package_tests = unittest.TestLoader().discover(start_dir="tests")

    verbosity=1
    if verbose:
        verbosity=2

    unittest.TextTestRunner(verbosity=verbosity).run(package_tests)