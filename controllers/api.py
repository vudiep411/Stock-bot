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
    response = response.json()
    if 'price' in response:
        return float(response['price'])
    else:
        return -1


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

def most_watch():
    API_KEY = os.getenv('API_KEY')
    url = "https://yahoo-finance15.p.rapidapi.com/api/yahoo/tr/trending"

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "yahoo-finance15.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers)
    response = response.json()
    display = ""
    i = 1
    quotes = response[0]["quotes"][0:50]
    for ticker in quotes:
        display += str(i) + ". " + ticker + "\n"
        i += 1
    return display
    
def most_active():
    API_KEY = os.getenv('API_KEY')
    url = "https://yahoo-finance15.p.rapidapi.com/api/yahoo/co/collections/most_actives"
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "yahoo-finance15.p.rapidapi.com"
    }

    res = ""
    response = requests.request("GET", url, headers=headers)
    response = response.json()
    quotes = response["quotes"]
    i = 1
    for ticker in quotes:
        res += str(i) + ". " + ticker['symbol'] + "\n"
        i += 1

    return res