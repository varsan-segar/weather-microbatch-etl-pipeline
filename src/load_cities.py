from extract import fetch_weather_data
import psycopg
from dotenv import load_dotenv
import os

load_dotenv()

host_name = os.getenv("HOST_NAME")
dbname = os.getenv("DBNAME")
port = os.getenv("PORT")
user = os.getenv("USER")
password = os.getenv("PASSWORD")

def load_cities_data(cities_data):
    records = []

    for data in cities_data:
        records.append((
            data['name'], data['coord']['lat'], data['coord']['lon']
        ))

    conn = None

    try:
        with psycopg.connect(host = host_name, dbname = dbname, port=port, user=user, password=password) as conn:
            with conn.cursor() as cur:
                query = "INSERT INTO city(city_name, latitude, longitude) VALUES(%s, %s, %s) ON CONFLICT DO NOTHING;"

                cur.executemany(query, records)
    except Exception as e:
        print(e)
    finally:
        if conn:
            conn.close()