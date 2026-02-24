import psycopg
import logging
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

def load_cities_data(cities_data):
    logger.info("City data loading started")

    records = []

    for data in cities_data:
        records.append((
            data['name'], data['coord']['lat'], data['coord']['lon']
        ))

    conn = None

    try:
        with psycopg.connect(host = host, dbname = dbname, port=port, user=user, password=password) as conn:
            with conn.cursor() as cur:
                insert_query = "INSERT INTO city(city_name, latitude, longitude) VALUES(%s, %s, %s) ON CONFLICT (city_name) DO NOTHING;"

                cur.executemany(insert_query, records)
    except Exception as e:
        logger.exception(e)
    finally:
        if conn:
            conn.close()
    
    logger.info("City data loading finished successfully")