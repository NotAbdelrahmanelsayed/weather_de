import os
import sys
import logging
from pathlib import Path
from weather_etl.utils import read_config
from configparser import ConfigParser

def setup_logging() -> logging.Logger:
    parser = ConfigParser()
    read_config(parser)
    log_path = Path(parser.get("logging", "path"))

    os.makedirs(log_path, exist_ok=True)
    logging_format = "[%(asctime)s: %(levelname)s: [%(module)s]: %(message)s]"
    
    logging.basicConfig(
        level=logging.INFO,
        format=logging_format,
        handlers=[
            logging.FileHandler(os.path.join(log_path, 'running_logs.log')),
            logging.StreamHandler(sys.stdout)
        ]
    )
    logger = logging.getLogger('weather_etl')
    return logger
