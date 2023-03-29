from controllers.api import get_price

def add_user(cur, user_id):
    cur.execute("SELECT * FROM trader WHERE id=%s;", (user_id,))
    result = cur.fetchone()
    if not result:
        cur.execute("INSERT INTO trader (id, cash) VALUES (%s, %s);", (user_id, 10000.00))
        return False
    return True


def buy_shares(cur, user_id, symbol, amount):
    price = get_price(symbol)

    if price != -1:
        enough_cash = False
        # Check Cash
        cur.execute("SELECT * FROM trader WHERE id=%s", (user_id,))
        user_data = cur.fetchone()
        cash = float(user_data[1])
        if user_data:
            enough_cash = False if cash < amount * price else True

        if enough_cash:
            new_cash = cash - amount * price
            cur.execute("SELECT * FROM inventory WHERE user_id=%s AND symbol=%s;", (user_id, symbol))
            result = cur.fetchone()
            
            if not result:
                cur.execute("""
                    INSERT INTO inventory (user_id, symbol, num_of_shares, avg_cost, total_cost) 
                    VALUES (%s, %s, %s, %s, %s);
                    """ , (user_id, symbol, amount, (price * amount) / amount, (price * amount))) 
            else:
                num_of_shares = int(result[2]) + amount
                total_cost = float(result[4]) + price * amount
                avg_cost = total_cost / num_of_shares

                cur.execute("""
                UPDATE inventory SET num_of_shares=%s, avg_cost=%s, total_cost=%s
                WHERE user_id=%s AND symbol=%s;
                """, (num_of_shares, avg_cost, total_cost, user_id, symbol))

            cur.execute("""
            INSERT INTO transactions (user_id, symbol, num_of_shares, price, date) VALUES (%s, %s, %s, %s, NOW())
            """, (user_id, symbol, amount, price))
            cur.execute("UPDATE trader SET cash=%s WHERE id=%s;", (new_cash, user_id))
            return True
        
        else:
            return False

def sell_shares(cur, user_id, symbol, amount):
    price = get_price(symbol)
    if price != -1:
        cur.execute("SELECT * FROM inventory WHERE user_id=%s AND symbol=%s;", (user_id, symbol))
        result = cur.fetchone()
        if not result:
            return False
        else:
            no_of_shares = float(result[2])
            if no_of_shares < amount:
                return False
            else:
                new_no_of_shares = no_of_shares - amount
                new_total_cost = float(result[4]) - float(result[3])

                cur.execute("SELECT * FROM trader WHERE id=%s", (user_id,))
                user_data = cur.fetchone()
                cash = float(user_data[1])  
                new_cash = cash + price * amount    

                cur.execute("""
                UPDATE inventory SET num_of_shares=%s, total_cost=%s WHERE user_id=%s AND symbol=%s;
                """, (new_no_of_shares, new_total_cost, user_id, symbol))

                cur.execute("UPDATE trader SET cash=%s WHERE id=%s;",(new_cash, user_id))

                cur.execute("""
                INSERT INTO transactions (user_id, symbol, num_of_shares, price, date) VALUES (%s, %s, %s, %s, NOW())
                """, (user_id, symbol, amount, price))
                return True
    else: 
        return False


def get_user_pf(cur, user_id):
    cur.execute("SELECT * FROM inventory WHERE user_id=%s;", (user_id,))
    result = cur.fetchall()
    return result
    

def get_cash(cur, user_id):
    cur.execute("SELECT * FROM trader WHERE id=%s;", (user_id,))
    result = cur.fetchone()
    return result
