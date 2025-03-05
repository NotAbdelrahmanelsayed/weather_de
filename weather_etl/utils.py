import os
from pathlib import Path

def get_config_path():
    """Returns the test config path or the original configuration file"""
    return os.environ.get("TEST_CONFIG", "configuration.conf")

def read_config(parser):
    config_path = get_config_path()
    parser.read(config_path)
    return parser