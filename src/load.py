import psycopg
import logging
from tenacity import retry, stop_after_attempt, wait_exponential
from config import DB_CONFIG

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

format = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")

file_handler = logging.FileHandler("./logs/etl.log")
file_handler.setFormatter(format)

logger.addHandler(file_handler)

host = DB_CONFIG['host']
dbname = DB_CONFIG['dbname']
port = DB_CONFIG['port']
user = DB_CONFIG['user']
password = DB_CONFIG['password']

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
def load_weather_data(cleaned_data):
    logger.info("Weather data loading started")

    conn = None

    try:
        with psycopg.connect(host=host, dbname=dbname, port=port, user=user, password=password) as conn:
            with conn.cursor() as cur:
                select_query = "SELECT city_name, city_id FROM city;"
                cur.execute(select_query)
                
                rows = cur.fetchall()
                city_id = {city_name: city_id for city_name, city_id in rows}
                
                cleaned_data['city_id'] = cleaned_data['city'].map(city_id)
                cleaned_data = cleaned_data.drop(columns = ['city'])
                cleaned_data = cleaned_data[[
                    'city_id',
                    'weather_description',
                    'temp_c',
                    'temp_feels_like_c',
                    'humidity_percentage',
                    'pressure_hpa',
                    'wind_speed',
                    'recorded_at'
                ]]
                cleaned_data = list(cleaned_data.itertuples(index = False, name = None))

                insert_query = """
                INSERT INTO weather(city_id, weather_description, temperature_c, temperature_feels_like_c, humidity_percentage, pressure_hpa, wind_speed, recorded_at)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (city_id, recorded_at) DO NOTHING;
                """
                cur.executemany(insert_query, cleaned_data)
    except Exception as e:
        logger.exception(e)
        raise e
    finally:
        if conn:
            conn.close()
    
    logger.info("Weather data loading finished successfully")