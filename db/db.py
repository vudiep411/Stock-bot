import psycopg2
from dotenv import load_dotenv
import os

def get_con():
    load_dotenv()
    DATABASE_URL = os.getenv("DATABASE_URL")
    conn = psycopg2.connect(DATABASE_URL)
    return conn