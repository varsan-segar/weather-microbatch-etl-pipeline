import requests
import logging
from tenacity import retry, stop_after_attempt, wait_exponential
from config import API_KEY

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

format = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")

file_handler = logging.FileHandler("./logs/etl.log")
file_handler.setFormatter(format)

logger.addHandler(file_handler)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=2, min=2, max=30))
def fetch_city_weather_data(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        return response.json()
    except Exception:
        logger.debug(f"Retry weather data extraction for city {city}")
        raise


def fetch_weather_data(cities):
    logger.info("Weather data extraction started")

    weather_data = []

    for city in cities:
        try:
            data = fetch_city_weather_data(city=city)
            weather_data.append(data)
            logger.info(f"Weather data for city {city} extracted successfully")
        except Exception as e:
            logger.exception(f"An error occurred for city {city}: {e}")
            continue
    
    logger.info("Weather data extraction finished successfully")
    
    return weather_data