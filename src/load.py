import psycopg
from config import DB_CONFIG

host = DB_CONFIG['host']
dbname = DB_CONFIG['dbname']
port = DB_CONFIG['port']
user = DB_CONFIG['user']
password = DB_CONFIG['password']

def load_weather_data(cleaned_data):
    conn = None

    try:
        with psycopg.connect(host=host, dbname=dbname, port=port, user=user, password=password) as conn:
            with conn.cursor() as cur:
                select_query = "SELECT city_name, city_id FROM city;"
                cur.execute(select_query)
                
                rows = cur.fetchall()
                city_id = {city_id: city_name for city_id, city_name in rows}
                
                cleaned_data['city'] = cleaned_data['city'].map(city_id)
                cleaned_data = list(cleaned_data.itertuples(index = False, name = None))

                insert_query = """
                INSERT INTO weather(city_id, weather_description, temperature_c, temperature_feels_like_c, humidity_percentage, pressure_hpa, wind_speed, recorded_at)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (city_id, recorded_at) DO NOTHING;
                """
                cur.executemany(insert_query, cleaned_data)
    except Exception as e:
        print(e)
    finally:
        if conn:
            conn.close()