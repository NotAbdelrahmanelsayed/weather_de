from unittest.mock import patch, Mock
import os
import unittest
from weather_etl.extract import main
from weather_etl.utils import read_config
from configparser import ConfigParser
from pathlib import Path

class TestExtract(unittest.TestCase):

    def setUp(self):
        """Set up test environment before each test."""
        os.environ["TEST_CONFIG"] = "test_config.conf"  # Set the test config file

        self.parser = ConfigParser()
        read_config(self.parser)  # Reads from the test config

        self.data_dir = Path(self.parser.get("data_dir", "path"))
        self.test_file_path = self.data_dir / "weather.csv"

        # Ensure the test directory exists
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Remove old test files
        if self.test_file_path.exists():
            self.test_file_path.unlink()

    def tearDown(self):
        """Clean up after each test."""
        if self.test_file_path.exists():
            self.test_file_path.unlink()

    @patch("requests.get")
    def test_valid_request(self, mock_get):
        """Test if the extract function correctly fetches and saves data."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "datetime,temp\n2025-03-10,25.0"
        mock_get.return_value = mock_response  # Simulate API response

        main()  # Run extraction

        # Verify request was made
        mock_get.assert_called_once()

        # Verify that the file is created and contains expected data
        self.assertTrue(self.test_file_path.exists(), "Weather data file was not created.")
        
        with open(self.test_file_path, "r") as file:
            content = file.read()
        
        self.assertIn("datetime,temp", content, "CSV file does not contain expected headers.")
        self.assertIn("2025-03-10,25.0", content, "CSV file does not contain expected data.")

if __name__ == "__main__":
    unittest.main()


# from unittest.mock import patch, Mock
# import os
# import unittest
# from weather_etl.extract import main
# from weather_etl.utils import read_config
# from configparser import ConfigParser
# from pathlib import Path

# class TestExtract(unittest.TestCase):
#     def setUp(self):
#         parser = ConfigParser()
#         read_config(parser, "conftest.conf")
#         data_dir = Path(parser.get("data_dir", "path"))
        
#         # Create the dir if not exist
#         data_dir.mkdir(exist_ok=True, parents=True)

#     @patch("requests.get")
#     def test_valid_request(self, mock_get):
#         mock_response = Mock()
#         mock_response.status_code = 200
#         mock_response.text = "datetime,temp\n2025-03-10,25.0"

#         # Simulate API response
#         mock_get.return_value = mock_response
        
#         # Verify request was made
#         mock_get.assert_called_once()

#         self.assertTrue()
#         # test extract
#         main()
        
    
# if __name__ == "__main__":
#     unittest.main()