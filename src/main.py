from extract import fetch_weather_data
from transform import tranform_weather_data
from load import load_weather_data
from config import cities

weather_data = fetch_weather_data(cities=cities)
cleaned_data = tranform_weather_data(weather_data=weather_data)
load_weather_data(cleaned_data=cleaned_data)