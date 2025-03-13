import pytest
import shutil
from pathlib import Path


@pytest.fixture(scope="session")
def temp_data_dir():
    """Fixture to use a fixed absolute directory for testing."""
    fixed_dir = Path("tests/data")

    # Ensure the directory is clean before running tests
    if fixed_dir.exists():
        shutil.rmtree(fixed_dir)  
    fixed_dir.mkdir(parents=True, exist_ok=True)  

    yield fixed_dir  

    shutil.rmtree(fixed_dir, ignore_errors=True)
