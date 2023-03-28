import psycopg2
from dotenv import load_dotenv
import os
from db.queries import *

def get_con():
    load_dotenv()
    DATABASE_URL = os.getenv("DATABASE_URL")
    conn = psycopg2.connect(DATABASE_URL)
    return conn

async def handle_buy_one(interaction, symbol, user_id):
    conn = get_con()
    cur = conn.cursor()
    add_user(cur, user_id)
    buy_shares(cur, user_id, symbol, 1)
    await interaction.response.send_message(f"Bought 1 share of {symbol}!")
    conn.commit()
    cur.close()
    conn.close()