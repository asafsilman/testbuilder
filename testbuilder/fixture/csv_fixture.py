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

        self.fixture_data = pandas.read_csv(csv_path, **kwargs)
        super().__init__(fixture_name)

    def get_value(self, row, column):
        """Get the value from the fixture
        
        Arguments:
            row {int} -- row number
            column {str} -- Column name
        
        Returns:
            any -- Value from fixture
        """

        return self.fixture_data.iloc[row][column]
