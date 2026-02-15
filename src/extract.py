import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")

cities = ["Chennai", "Bangalore", "Hyderabad", "Mumbai", "Delhi"]

def fetch_weather_data(cities):
    weather_data = []

    for city in cities:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            weather_data.append(data)
        except Exception as e:
            print(f"An error occurred for city {city}: {e}")
    
    return weather_data