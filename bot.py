from dotenv import load_dotenv
import os
import discord
from discord.ui import Button, View, Modal
from controllers.api import *
from controllers.events import *
from controllers.docs import *
import datetime


load_dotenv()  # load variables from .env file

BOT_TOKEN = os.getenv("BOT_TOKEN")
intents = discord.Intents.all()
client = discord.Client(intents=intents)
start_time = datetime.time(hour=14, minute=30)
end_time = datetime.time(hour=21, minute=0)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    current_time = datetime.datetime.now().time()
    current_day = datetime.datetime.now().weekday()
    if message.author == client.user:
        return

    if message.content.startswith('#help'):
        documentation = bot_docs()
        embed = discord.Embed(title = "Stock-Bot | Help Menu", description=documentation)
        await message.channel.send(embed=embed, reference=message)

    #price
    elif message.content.startswith("#price"):
        ticker = message.content.split(' ')

        if len(ticker) > 1:
            price = get_price(ticker[1])
            button = Button(style=discord.ButtonStyle.green, label="Buy")
            user_id = str(message.author)
            button.callback = lambda i, **kwargs: handle_buy_one(i, symbol=ticker[1], user_id=user_id)

            view = View()
            view.add_item(button)

            if price != -1:
                await message.channel.send(f"**{ticker[1]}**: **${price}**", reference=message)
            else:
                await message.channel.send("Enter a valid symbol", reference=message) 

    #curex
    elif message.content.startswith("#curex"):
        strs = message.content.split(' ')
        if len(strs) == 3:
            currency = strs[1]
            amount = strs[2]

            rate = currency_conversion(currency, amount)
            if 'rate' in rate:
                data = currency.split('/')
                await message.channel.send(f"Conversion rate is: **{rate['rate']}** \n **{amount}** {data[0]} = **{rate['amount']}** {data[1]}", reference=message)
            else:
                await message.channel.send("Invalid params", reference=message)

    #pf
    elif message.content.startswith("#pf"):
        user_id = str(message.author)
        r = get_pf(user_id)
        display = ""
        for data in r:
            symbol = data["symbol"]
            qty = data["qty"]
            avg = data["avg"]
            formatted_str = f"**{symbol}**   **{qty}**  ---  `Avg cost`: **${avg}**\n"
            display += formatted_str
        display = "Empty!" if not display else display
        embed = discord.Embed(title="Your Porfolio", description=display, color=discord.Colour.green())
        await message.channel.send(embed=embed, reference=message)

    #buy
    elif message.content.startswith("#buy"):
        if (start_time <= current_time <= end_time) and current_day < 5 :
            user_id = str(message.author)
            strs = message.content.split(' ')
            if len(strs) == 3:
                amount = float(strs[1])
                symbol = strs[2].upper()
                can_buy = buy(symbol, user_id, amount)
                if can_buy:
                    await message.channel.send(f"Successfuly bought {amount} shares of **{symbol}**", reference=message)
                else:
                    await message.channel.send(f"Not enough cash to buy **{symbol}** or Invalid symbol", reference=message)
        else:
            await message.channel.send("Market Closed", reference=message)

    #sell
    elif message.content.startswith("#sell"):
        if (start_time <= current_time <= end_time) and current_day < 5:
            user_id = str(message.author)
            strs = message.content.split(' ')  
            if len(strs) >= 2:
                if strs[1] == "all":
                    sell_all(user_id)
                    await message.channel.send("You sold everything!", reference=message)
                elif len(strs) == 3:
                    amount = float(strs[1])
                    symbol = strs[2].upper()
                    can_sell = sell(symbol, user_id, amount)
                    if can_sell:
                        await message.channel.send(f"Successfuly sold {amount} shares of **{symbol}**", reference=message)
                    else:
                        await message.channel.send(f"Not enough shares to sell **{symbol}** or Invalid symbol", reference=message)
        else:
            await message.channel.send("Market Closed", reference=message)
    #cash
    elif message.content.startswith("#cash"):
        user_id = str(message.author)
        c = show_cash(user_id)
        await message.channel.send(f"*Your Cash*:\n**${c}**", reference=message)

    #tr
    elif message.content.startswith("#trs"):
        user_id = str(message.author)
        data = transactions(user_id)
        display=""
        for t in data:
            t_id = t['id']
            symbol = t["symbol"]
            qty = t['qty']
            price = t['price']
            date = t['date']
            action = 'BUY' if t['buy'] else 'SELL'
            trans = f"**{t_id} - ** {action} {symbol} at ${price} --- {qty} shares --- {date}\n"
            display += trans
        display = "Empty!" if not display else display
        embed = discord.Embed(title="Your Transactions", description=display, color=discord.Colour.green())
        await message.channel.send(embed=embed, reference=message)

    #time
    elif message.content.startswith("#time"):
        t = datetime.datetime.now()
        formatted_datetime = t.strftime("%m/%d/%y %H:%M:%S")
        await message.channel.send(f"Time: {formatted_datetime}", reference=message)

    elif message.content.startswith("#hello"):
        user_id = str(message.author)
        await message.channel.send(f"Hello Bitch", reference=message)


     

client.run(BOT_TOKEN)