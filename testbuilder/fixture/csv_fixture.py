from testbuilder.core.base.basefixtures import TBBaseFixture
import pandas

class CSVFixture(TBBaseFixture):
    def __init__(self, fixture_name, csv_path, **kwargs):
        """Create a fixture from CSV file using pandas.
        Additional options for loading csv can be passed to this constructor
        
        Arguments:
            fixture_name {str} - Name of fixture
            csv_path {str} -- Path to csv fixture
        """

        self.fixture_name = fixture_name
        self.fixture_data = pandas.read_csv(csv_path, **kwargs)

    def get_value(self, iteration, column):
        """Get the value from the fixture for the current iteration
        
        Arguments:
            iteration {int} -- Iteration number
            column {str} -- Column name
        
        Returns:
            any -- Value from fixture
        """

        return self.fixture_data.iloc[iteration][column]