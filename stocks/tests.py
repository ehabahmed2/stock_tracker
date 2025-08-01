from django.test import TestCase
from decouple import config
import requests
api_key = config('F_API_KEY')
symbol = 'TSLA' # hard coded for now. :)
url = f"https://financialmodelingprep.com/api/v3/quote-short/{symbol}?apikey={api_key}"
res = requests.get(url)
print(res.json())
