import requests
import logging
from config import API_KEY

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

format = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")

file_handler = logging.FileHandler("./logs/etl.log")
file_handler.setFormatter(format)

logger.addHandler(file_handler)

def fetch_weather_data(cities):
    logger.info("Weather data extraction started")

    weather_data = []

    for city in cities:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            weather_data.append(data)
        except Exception as e:
            logger.exception(f"An error occurred for city {city}: {e}")
    
    logger.info("Weather data extraction finished successfully")
    
    return weather_data