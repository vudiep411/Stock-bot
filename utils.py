import discord
import requests
import os


def get_price(ticker):
    API_KEY = os.getenv('API_KEY')
    url = "https://twelve-data1.p.rapidapi.com/price"

    querystring = {"symbol": ticker,"format":"json","outputsize":"30"}

    headers = {
    	"X-RapidAPI-Key": API_KEY,
    	"X-RapidAPI-Host": "twelve-data1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.json()


def currency_conversion(c, amount):
    API_KEY = os.getenv('API_KEY')
    url = "https://twelve-data1.p.rapidapi.com/currency_conversion"
    querystring = {"symbol": c,"amount":amount}
    headers = {
    	"X-RapidAPI-Key": API_KEY,
    	"X-RapidAPI-Host": "twelve-data1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.json()

    