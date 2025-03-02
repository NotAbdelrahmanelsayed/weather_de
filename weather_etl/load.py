import pandas as  pd
from sqlalchemy import create_engine, text
import psycopg2
from configparser import ConfigParser
import datetime
import os
from weather_etl.utils import read_config
from weather_etl.logs import logger

def main():
    # Load configuration file
    logger.info("Reading the configuration file")
    parser = ConfigParser()
    read_config(parser)

    # Load database configuration
    try:
        dbname = parser.get("postgres_config", "database")
        user = parser.get("postgres_config", "username")
        password = parser.get("postgres_config", "password")
        host = parser.get("postgres_config", "host")
        port = parser.get("postgres_config", "port")
        logger.info("postgress_config read.")
    except Exception as e:
        logger.error("Couldn't find 'postgres_config' in the configuration file")
    
    try:
        # Load dataset configuration
        path = parser.get("data_dir", "transformed")
        logger.info("data_dir config read.")
    except Exception as e:
         logger.error("Couldn't find 'data_dir' in the configuration file")
         
    # make Connection
    DATABASE_URL = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
    try:
        engine = create_engine(DATABASE_URL)
        logger.info("Engine initiated.")
    except Exception as e:
        logger.error(f"Failed to create engine... {e}")
    
    connection = engine.connect()

    # Reading the data
    logger.info("Reading the transformed data")
    try: 
        df = pd.read_csv(path)
        logger.info(f"Successfully read the dataframe with columns {df.columns}")
    except Exception as e:
         logger.error(f"Couldn't read the csv file {path} | {e}")
         return # Exit the function early if reading fails

    try:
        df.to_sql('weather', con=connection, if_exists='append', index=False)
        logger.info("Data loaded successfully into the database")
    except Exception as e:
        logger.error(f"Error loading df to database | {e}")

    # Get the last updated record
    # query = text("select max(timestamp) from weather")
    # conn.execute(query)
    # maximum_timestamp = int(conn.execute(query).fetchone()[0]) or 0 

    # Select the new data to insert on the database
    # df = df.query(f"timestamp > {maximum_timestamp}")
    

if __name__ == "__main__":
       main()
    