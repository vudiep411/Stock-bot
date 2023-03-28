from dotenv import load_dotenv
from db.queries import *
from db.db import get_con


async def handle_buy_one(interaction, symbol, user_id):
    conn = get_con()
    cur = conn.cursor()
    add_user(cur, user_id)
    buy_shares(cur, user_id, symbol, 1)
    user_mention = interaction.user.mention
    await interaction.response.send_message(f"{user_mention} bought 1 share of {symbol}!")
    conn.commit()
    cur.close()
    conn.close()