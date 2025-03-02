import configparser
from pathlib import Path

parser = configparser.ConfigParser()
config_path = Path("configuration.conf")
def read_config(parser, config_path=config_path):
    parser.read(config_path)
    return parser

# # Load database configuration
# dbname = parser.get("postgres_config", "database")
# user = parser.get("postgres_config", "username")
# password = parser.get("postgres_config", "password")
# host = parser.get("postgres_config", "host")
# port = parser.get("postgres_config", "port")