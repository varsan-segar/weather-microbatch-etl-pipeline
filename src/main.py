import logging
from extract import fetch_weather_data
from transform import transform_weather_data
from load import load_weather_data
from config import cities
from logger_config import setup_logger

setup_logger()

logger = logging.getLogger(__name__)

logger.info("ETL pipeline started")

weather_data = fetch_weather_data(cities=cities)
cleaned_data = transform_weather_data(weather_data=weather_data)
load_weather_data(cleaned_data=cleaned_data)

logger.info("ETL pipeline finished")