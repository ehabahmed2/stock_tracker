from django.test import TestCase
import requests
from decouple import config

symbol = 'TSLA' # hard coded for now. :)
# define our api and configurateion
api_key = config('F_API_KEY')

url = f"https://financialmodelingprep.com/api/v3/quote-short/{symbol}?apikey={api_key}"
response = requests.get(url)
data = response.json()
if data:
    price = data[0].get('price')
    print(price)
    print(data)
