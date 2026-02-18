import pandas as pd
from datetime import datetime

def tranform_weather_data(weather_data):
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

    return pd.DataFrame(records)