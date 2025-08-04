from decouple import config
import requests
from celery import shared_task
from .models import Stock
from django.utils import timezone
from alerts.models import Alert

# define our api and configurateion
api_key = config('F_API_KEY')


@shared_task
def fetch_stock_prices():
    # Filter stocks that have active alerts
    stock_ids_with_alerts = Alert.objects.filter(is_active=True).values_list('stock_id', flat=True).distinct()
    stocks = Stock.objects.filter(id__in=stock_ids_with_alerts)

    for stock in stocks:
        url = f"https://financialmodelingprep.com/api/v3/quote-short/{stock.symbol}?apikey={api_key}"
        response = requests.get(url)
        data = response.json()

        try:
            if data:
                price = data[0]["price"]
                stock.last_price = price
                stock.updated_at = timezone.now()
                stock.save()
            else:
                print(f"No valid price data for symbol: {stock.symbol} — received: {data}")
        except Exception as e:
            print(f"Error fetching price for symbol: {stock.symbol} — {e}")
