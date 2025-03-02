import pandas as pd
from configparser import ConfigParser
import os 
from weather_etl.utils import read_config
from weather_etl.logs import logger

def main():
    # Read the configuration
    logger.info("Reading the configuration file")
    parser = ConfigParser()
    read_config(parser)

    # Defining data pathes
    try:
        data_dir = parser.get("data_dir", "path")
        data_path = os.path.join(data_dir, "weather.csv")
        logger.info("Configuration read.")
    except Exception as e:
        logger.error("Couldn't find 'data_dir' in the configuration file")
        
    
    # Reading the data
    logger.info("Reading the transofmr data")
    try: 
        df = pd.read_csv(data_path,  header=0, low_memory=False)
        logger.info(f"Successfully read the dataframe with columns {df.columns}")
    except Exception as e:
         logger.error(f"Couldn't read the csv file {data_path} | {e}")
         return # Exit the function early if reading fails

    # Drop duplicates
    if not df.empty:
        logger.info("Drop duplicates from the dataframe..")
        df.drop_duplicates(inplace=True)
    else:
        logger.warning("DataFrame is empty. skipping the rest of transformations")
        return # Exit the function if df is empty.

    # Drop unncessary columns
    columns_to_drop = ["stations", "preciptype"]
    existing_cols = [col for col in columns_to_drop if col in df.columns]
    if existing_cols:
        logger.info(f"Drop unncessary columns {existing_cols}....")
        df.drop(columns=columns_to_drop, inplace=True)
    else:
        logger.warning(f"columns {columns_to_drop} doesn't exist in {df.columns}.")
    
    # Replace arabic text with english.
    logger.info("replace arabic column with english")
    if "name" in df.columns:
        df["name"] = df.name.str.replace("مصر", "Egypt")
        logger.info("Replacment successful.")
    else:
         logger.warning(f"Column 'name' not found in: {list(df.columns)}")

    # Convert date column to datetime
    logger.info("Convert date time.....")
    if "datetime" in df.columns:
        df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
        logger.info("conversion successful.")
    else:
         logger.warning(f"Column 'datetime' not found in: {list(df.columns)}")

    logger.info("Creating timestmap column.....")
    # Create timestamp
    if "datetime" in df.columns:
        df["timestamp"] = df["datetime"].values.astype("int64") // 10 ** 9
        logger.info("timestamp created succesfully.")
    else:
        logger.warning("Column 'datetime' not found.")

    # Set the timestamp as index
    if "timestamp" in df.columns:
        df.set_index("timestamp", inplace=True)
        logger.info("Set 'timestamp' as index.")
    else:
        logger.warning("'timestamp' column is missing. Cannot set index.")


    # Save the transformed data
    transformed_path = os.path.join(data_dir, "weather_transformed.csv")
    try:
        df.to_csv(transformed_path, index=False)
        logger.info(f"Transformed data successfull saved in {transformed_path}.")
    except Exception as e:
        logger.info(f"Failed to save the transformed data to {transformed_path} | {e}.")

if __name__ == "__main__":
       main()