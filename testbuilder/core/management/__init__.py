"""
Placeholder for future implementation
"""

from .load_engine import load_engine

import unittest

def run_test_case(file, file_type, profile):
    engine = load_engine()

    tests = engine.create_tests(file, file_type, profile)

    for test in tests:
        if test.run_test:
            for _ in range(test.test_iterations):
                test.run()
                test.configure_next_iteration()

def run_unittests(verbose):
    package_tests = unittest.TestLoader().discover(start_dir="tests")

    verbosity=1
    if verbose:
        verbosity=2

    unittest.TextTestRunner(verbosity=verbosity).run(package_tests)