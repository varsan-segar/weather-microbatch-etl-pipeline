import pandas as pd
from datetime import datetime

def tranform_weather_data(weather_data):
    records = []

    for data in weather_data:
        recorded_at = pd.to_datetime(data['dt'], utc=True, yearfirst=True, unit='s').tz_convert('Asia/Kolkata')
        records.append({
            'city':data['name'],
            'description':data['weather'][0]['main'],
            'temperature':round((data['main']['temp']) - 273.15, 2),
            'humidity':data['main']['humidity'],
            'recorded_at':datetime.strftime(recorded_at, format = "%Y-%m-%d %H:%M")
        })

    df = pd.DataFrame(records)

    return df