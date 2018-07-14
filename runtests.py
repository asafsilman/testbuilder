"""Run all tests under tests directory
"""

import unittest

package_tests = unittest.TestLoader().discover(start_dir="tests")

if __name__=="__main__":
    unittest.TextTestRunner().run(package_tests)