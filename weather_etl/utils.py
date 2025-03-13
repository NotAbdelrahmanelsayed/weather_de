import os
from pathlib import Path

def get_config_path():
    """Ensure the correct config file is used."""
    config_path = os.environ.get("TEST_CONFIG", "configuration.conf")  # Read from env
    print(f"Using config file: {config_path}")  # Debugging print
    return config_path
def read_config(parser, config_path=None): 
    if config_path is None:
        config_path = get_config_path() 
    parser.read(config_path) 
    return parser
