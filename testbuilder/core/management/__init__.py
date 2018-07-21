"""
Placeholder for future implementation
"""

from .load_engine import load_engine

import unittest

def run_test_case(file, file_type, profile):
    engine = load_engine()

    test = engine.create_test(file, file_type, profile)

    test.run()

def run_unittests(verbose):
    package_tests = unittest.TestLoader().discover(start_dir="tests")

    verbosity=1
    if verbose:
        verbosity=2

    unittest.TextTestRunner(verbosity=verbosity).run(package_tests)