from fastapi import FastAPI
import psycopg
from config import host, dbname, port, user, password

app = FastAPI()

def query_database(query, params):
    try:
        with psycopg.connect(host=host, dbname=dbname, port=port, user=user, password=password) as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                row = cur.fetchall()

                return row
    except Exception as e:
        print(e)
    
    return None

@app.get("/current")
def get_current_temperature(city: str):
    data_query = "SELECT * FROM weather INNER JOIN city ON weather.city_id = city.city_id WHERE city_name = %s ORDER BY ingested_at DESC LIMIT 1"
    params = (city,)
    data = query_database(query=data_query, params=params)

    weather_description = data[0][2]
    temperature_c = data[0][3]
    temperature_feels_like_c = data[0][4]
    humidity_percentage = data[0][5]
    pressure_hpa = data[0][6]
    wind_speed = data[0][7]
    recorded_at = data[0][8]

    return {
        "weather_description": weather_description,
        "temperature_c": temperature_c,
        "temperature_feels_like_c": temperature_feels_like_c,
        "humidity_percentage": humidity_percentage,
        "pressure_hpa": pressure_hpa,
        "wind_speed": wind_speed,
        "recorded_at": recorded_at
    }

@app.get("/trends")
def get_last_24h_trend(city: str):
    data_query = "SELECT temperature_c, temperature_feels_like_c, humidity_percentage, wind_speed, recorded_at FROM weather INNER JOIN city ON weather.city_id = city.city_id WHERE city_name = %s AND ingested_at >= NOW() - INTERVAL '24 hours'"
    params = (city,)
    data = query_database(query=data_query, params=params)

    tempertaure_c = []
    temperature_feels_like_c = []
    humidity_percentage = []
    wind_speed = []
    recorded_at = []

    for i in range(len(data)):
        tempertaure_c.append(data[i][0])
        temperature_feels_like_c.append(data[i][1])
        humidity_percentage.append(data[i][2])
        wind_speed.append(data[i][3])
        recorded_at.append(data[i][4])
    
    return {
        "temperature_c": tempertaure_c,
        "temperature_feels_like_c": temperature_feels_like_c,
        "humidity_percentage": humidity_percentage,
        "wind_speed": wind_speed,
        "recorded_at": recorded_at
    }