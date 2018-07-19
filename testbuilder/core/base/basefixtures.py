"""Base Testbuilder Fixtures"""

class TBBaseFixture:
    fixture_data=None

    def load_fixture(self, *args):
        """Load fixture data"""
        pass

    def get_value(self, iteration, column):
        """
        Loads value from fixture
        
        Arguments:
            iteration {int} -- Iteration number
            column {str} -- Column Name
        """

        pass
