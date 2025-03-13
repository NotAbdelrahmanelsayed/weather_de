import os
from pathlib import Path
print("**"*50)
print("**"*50)
def get_config_path():
    """Returns the test config path or the original configuration file"""
    if "PYTEST_VERSION" in os.environ:  # Detect when pytest is running
        return "tests/test_config.conf"
    return os.environ.get("TEST_CONFIG", "configuration.conf")

def read_config(parser, config_path=get_config_path()):
    parser.read(config_path)
    return parser