import requests
import pandas as pd
from io import StringIO
from configparser import ConfigParser
from pathlib import Path
from weather_etl.utils import read_config
from weather_etl.logs import logger
import os

def main():
       # Read the configuration
       parser = ConfigParser()
       read_config(parser)
       # Parse the configuration
       try:
              logger.info("Reading the configuration data")
              api_key = parser.get("visual_crossing", "key")
              country = parser.get("visual_crossing", "country")
              data_dir = Path(parser.get("data_dir", "path"))
              logger.info("Successfully read the configuration")
       except Exception as e:
              logger.exception(f"Error reading the configuration {e}")

       # Confirm the data directory exists
       data_dir.mkdir(exist_ok=True, parents=True)

       # Define the URL 
       url = ("https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/"
              + "timeline/" + country
              + "?unitGroup=metric&include=hours&key=" + api_key + "&contentType=csv")

       logger.info("Making a request to Visual Crossing API..")
       # Make the request
       response = requests.get(url)
       
       # Check if the request was successful
       if response.status_code == 200:
              logger.info("The request was succssed")
              response.encoding = "utf-8"
              # Save the data as a csv. 
              csv_data = StringIO(response.text)
              df = pd.read_csv(csv_data)
              data_path = Path(f"{data_dir}/weather.csv")
              if data_path.exists() and data_path.stat().st_size > 0:
                     df.to_csv(data_path, mode='a', index=False, header=False)
              else:
                     df.to_csv(data_path, index=False, header=True)


       else:
              logger.exception(f"{response.raise_for_status()}")
              
if __name__ == "__main__":
       main()