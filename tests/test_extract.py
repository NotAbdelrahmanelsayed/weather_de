from unittest.mock import patch, Mock
import os
from weather_etl.extract import main
from configparser import ConfigParser
from pathlib import Path
import pytest
import shutil

@pytest.fixture(scope="session") # Keep data for all tests in the session
def temp_data_dir(tmp_path_factory):
    "Fixture to create a temporary data dir for testing"
    print("Creating the folder")
    folder = Path(tmp_path_factory.mktemp("test_data"))
    yield folder
    print("removing the temp folder")
    shutil.rmtree(folder, ignore_errors=True)

@patch("requests.get")
def test_valid_request(mock_get, temp_data_dir):
    """Test if the extract function correctly fetches and saves data."""
    test_config_path = "tests/test_config.conf"
    parser = ConfigParser()
    parser.read(test_config_path)
    parser.set("data_dir", "path", str(temp_data_dir))

    # Write the temp
    with open(test_config_path, "w") as configfile:
        parser.write(configfile)

    test_file_path = temp_data_dir / "weather.csv"

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = "datetime,temp\n2025-03-10,25.0"
    mock_get.return_value = mock_response  # Simulate API response

    main()  # Run extraction

    # Verify request was made
    mock_get.assert_called_once()

    # Verify that the file is created and contains expected data
    assert test_file_path.exists(), "Weather data file was not created."
    
    with open(test_file_path, "r") as file:
        content = file.read()
    
    # Assert the 
    assert "datetime,temp" in content, "CSV file does not contain expected headers."
    assert "2025-03-10,25.0" in content, "CSV file does not contain expected data."
