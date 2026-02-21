from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")

DB_CONFIG = {
    'host':os.getenv("HOST_NAME"),
    'dbname':os.getenv("DBNAME"),
    'port':os.getenv("PORT"),
    'user':os.getenv("USER"),
    'password':os.getenv("PASSWORD")
}

cities = ["Chennai", "Bangalore", "Hyderabad", "Mumbai", "Delhi"]