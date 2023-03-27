from dotenv import load_dotenv
import os
import discord
from utils import *

load_dotenv()  # load variables from .env file

BOT_TOKEN = os.getenv("BOT_TOKEN")
intents = discord.Intents.all()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith("#price"):
        ticker = message.content.split(' ')
        if len(ticker) > 1:
            price = get_price(ticker[1])
            if "price" in price:
                price = price["price"]
                await message.channel.send(f"{ticker[1]}: ${price}", reference=message)
            else:
                await message.channel.send("Enter a valid symbol", reference=message) 

client.run(BOT_TOKEN)