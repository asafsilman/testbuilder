"""Base Testbuilder Fixtures"""

class TBBaseFixture:
    fixture_data=None
    fixture_name=""

    def get_value(self, iteration, column):
        """
        Loads value from fixture
        
        Arguments:
            iteration {int} -- Iteration number
            column {str} -- Column Name
        """

        pass

    def __repr__(self):
        return f"<Fixture '{self.fixture_name}'>"

    def __str__(self):
        return f"<Fixture '{self.fixture_name}'>"