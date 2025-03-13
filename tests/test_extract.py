from unittest.mock import patch, Mock
import os
import unittest
from weather_etl.extract import main
from weather_etl.utils import read_config
from configparser import ConfigParser
from pathlib import Path
import pytest

@pytest.fixture
def temp_data_dir(tmpdir):
    "Fixture to create a temporary data dir for testing"
    return tmpdir.mkdir("test_data")

@patch("requests.get")
def test_valid_request(mock_get, temp_data_dir):
    """Test if the extract function correctly fetches and saves data."""
    data_dir = Path(temp_data_dir)
    test_file_path = data_dir / "weather.csv"

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
