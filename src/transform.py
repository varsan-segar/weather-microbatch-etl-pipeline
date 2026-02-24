import pandas as pd
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

format = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")

file_handler = logging.FileHandler("./logs/etl.log")
file_handler.setFormatter(format)

logger.addHandler(file_handler)

def tranform_weather_data(weather_data):
    logger.info("Weather data transformation started")

    records = []

    for data in weather_data:
        records.append({
            'city':data['name'],
            'weather_description':data['weather'][0]['main'],
            'temp_c':round((data['main']['temp']) - 273.15, 2),
            'temp_feels_like_c':round((data['main']['feels_like']) - 273.15, 2),
            'humidity_percentage':data['main']['humidity'],
            'pressure_hpa':data['main']['pressure'],
            'wind_speed':round(data['wind']['speed'], 2),
            'recorded_at':pd.to_datetime(data['dt'], utc=True, unit='s')
        })

    logger.info("Weather data transformation finished successfully")

    return pd.DataFrame(records)