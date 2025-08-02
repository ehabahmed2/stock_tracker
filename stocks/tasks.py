from decouple import config
import requests
from celery import shared_task
from .models import Stock

# define our api and configurateion
api_key = config('F_API_KEY')


@shared_task
def fetch_stock_prices(): 
    # get all of the stocks we have in db
    stocks = Stock.objects.all()
    # look for all symbols and their prices
    for stock in stocks:
        url = f"https://financialmodelingprep.com/api/v3/quote-short/{stock.symbol}?apikey={api_key}"
        response = requests.get(url)
        data = response.json()
        if data:
            price = data[0].get("price")
            stock.last_price = price
            stock.save()

