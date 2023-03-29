from dotenv import load_dotenv
from db.queries import *
from db.db import get_con


async def handle_buy_one(interaction, symbol, user_id):
    conn = get_con()
    cur = conn.cursor()
    add_user(cur, user_id)
    can_buy = buy_shares(cur, user_id, symbol, 1)
    user_mention = interaction.user.mention
    if can_buy:
        await interaction.response.send_message(f"{user_mention} bought 1 share of {symbol}!")
    else:
        await interaction.response.send_message(f"{user_mention} Not enough cash to buy {symbol} or Invalid symbol")
    conn.commit()
    cur.close()
    conn.close()


def get_pf(user_id):
    conn = get_con()
    cur = conn.cursor()
    add_user(cur, user_id)    
    result = get_user_pf(cur, user_id)
    conn.commit()
    cur.close()
    conn.close()
    formatted_r = []
    for data in result:
        m = {
            "symbol" : data[1],
            "qty": data[2],
            "avg": data[3]
        }
        formatted_r.append(m)
    return formatted_r


def show_cash(user_id):
    conn = get_con()
    cur = conn.cursor()
    cash = get_cash(cur, user_id)
    conn.commit()
    cur.close()
    conn.close()
    return cash[1]

def buy(symbol, user_id, amount):
    conn = get_con()
    cur = conn.cursor()
    add_user(cur, user_id)   
    can_buy = buy_shares(cur, user_id, symbol, amount)
    conn.commit()
    cur.close()
    conn.close()
    return can_buy

def sell(symbol, user_id, amount):
    conn = get_con()
    cur = conn.cursor()    

    user_exist = add_user(cur, user_id)
    if not user_exist:
        return False
    
    can_sell = sell_shares(cur, user_id, symbol, amount)
    conn.commit()
    cur.close()
    conn.close()
    return can_sell