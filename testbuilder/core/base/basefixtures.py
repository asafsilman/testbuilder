"""Base Testbuilder Fixtures"""

class TBBaseFixture:
    def __init__(self, fixture_name):
        self.fixture_name=fixture_name

    def get_value(self, iteration, column):
        """
        Loads value from fixture
        
        Arguments:
            iteration {int} -- Iteration number
            column {str} -- Column Name
        """
        raise NotImplementedError("Overwrite this function")

    def __repr__(self):
        return f"<Fixture '{self.fixture_name}'>"

    def __str__(self):
        return f"<Fixture '{self.fixture_name}'>"