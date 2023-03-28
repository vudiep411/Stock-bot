from utils.api import get_price

def add_user(cur, user_id):
    cur.execute("SELECT * FROM trader WHERE id=%s;", (user_id,))
    result = cur.fetchone()

    if not result:
        cur.execute("INSERT INTO trader (id, cash) VALUES (%s, %s);", (user_id, 10000.00))


def buy_shares(cur, user_id, symbol, amount):
    price = get_price(symbol)

    if price != -1:
        cur.execute("SELECT * FROM inventory WHERE user_id=%s AND symbol=%s;", (user_id, symbol))
        result = cur.fetchone()

        if not result:
            cur.execute("""
                INSERT INTO inventory (user_id, symbol, num_of_shares, avg_cost) 
                VALUES (%s, %s, %s, %s);
                """ , (user_id, symbol, amount, (price * amount))) 
        else:
            num_of_shares = int(result[2]) + amount
            avg_cost = (float(result[3]) + price * amount) / num_of_shares
            cur.execute("""
            UPDATE inventory SET num_of_shares=%s, avg_cost=%s
            WHERE user_id=%s AND symbol=%s;
            """, (num_of_shares, avg_cost, user_id, symbol))

        cur.execute("""
        INSERT INTO transactions (user_id, symbol, num_of_shares, price, date) VALUES (%s, %s, %s, %s, NOW())
        """, (user_id, symbol, amount, price))



    

