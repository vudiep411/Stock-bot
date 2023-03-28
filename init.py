import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS inventory (
        user_id VARCHAR,
        symbol VARCHAR,
        num_of_shares INT,
        avg_cost REAL
    );
""")
cur.execute("""
    CREATE TABLE IF NOT EXISTS trader (
        id VARCHAR UNIQUE,
        cash REAL NOT NULL
    );
""")
cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id SERIAL PRIMARY KEY,
        user_id VARCHAR,
        symbol VARCHAR,
        num_of_shares INT,
        price REAL,
        date DATE
    );
""")


conn.commit()
cur.close()
conn.close()