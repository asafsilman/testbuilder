"""
Placeholder for future implementation
"""

import unittest

def run_test_case(file, file_type):
    pass

def run_unittests(verbose):
    package_tests = unittest.TestLoader().discover(start_dir="tests")

    verbosity=1
    if verbose:
        verbosity=2

    unittest.TextTestRunner(verbosity=verbosity).run(package_tests)