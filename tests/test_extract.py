from unittest.mock import patch, Mock
import os
from weather_etl.extract import main
from pathlib import Path
import pytest
import shutil

@pytest.fixture(scope="session")
def temp_data_dir():
    """Fixture to use a fixed absolute directory for testing."""
    fixed_dir = Path("tests/data")
    print(f"🔍 Using fixed test directory: {fixed_dir}")

    # Ensure the directory is clean before running tests
    if fixed_dir.exists():
        shutil.rmtree(fixed_dir)  
    fixed_dir.mkdir(parents=True, exist_ok=True)  

    yield fixed_dir  

    shutil.rmtree(fixed_dir, ignore_errors=True)

@patch("requests.get")
def test_valid_request(mock_get, temp_data_dir, monkeypatch):
    """Test if the extract function correctly fetches and saves data."""
    config_file = temp_data_dir.parent / "test_config.conf"
    monkeypatch.setenv("TEST_CONFIG", str(config_file))
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
    
    # Assert the content
    assert "datetime,temp" in content, "CSV file does not contain expected headers."
    assert "2025-03-10,25.0" in content, "CSV file does not contain expected data."
