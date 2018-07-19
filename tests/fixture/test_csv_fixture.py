from testbuilder.fixture.csv_fixture import CSVFixture

import os
import unittest

class TestCSVFixture(unittest.TestCase):
    def setUp(self):
        self.umrn_fixture_path = os.path.join(
            os.path.dirname(__file__),
            "fixtures",
            "sample_umrn_list.csv"
        )
        self.fixture = CSVFixture("Test Fixture", self.umrn_fixture_path)

    def test_get_value(self):
        umrn1 = self.fixture.get_value(0, "UMRN")
        firstname1 = self.fixture.get_value(0, "FirstName")
        lastname1 = self.fixture.get_value(0, "LastName")

        umrn2 = self.fixture.get_value(1, "UMRN")

        self.assertEqual(umrn1, "L2842343")
        self.assertEqual(firstname1, "Bob")
        self.assertEqual(lastname1, "Armstrong")

        self.assertEqual(umrn2, "K5345343")
