import logging
from extract import fetch_weather_data
from transform import transform_weather_data
from load import load_weather_data
from config import cities

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

format = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")

file_handler = logging.FileHandler("./logs/etl.log")
file_handler.setFormatter(format)

logger.addHandler(file_handler)

logger.info("ETL pipeline started")

weather_data = fetch_weather_data(cities=cities)
cleaned_data = transform_weather_data(weather_data=weather_data)
load_weather_data(cleaned_data=cleaned_data)

logger.info("ETL pipeline finished")