from django.core.management.base import BaseCommand
from stocks.models import Stock
from decouple import config
import requests

FMP_API_KEY = config('F_API_KEY')

SEED_STOCKS = [
    ('AAPL', 'Apple Inc.'),
    ('TSLA', 'Tesla Inc.'),
    ('GOOGL', 'Alphabet Inc.'),
    ('MSFT', 'Microsoft Corporation'),
    ('AMZN', 'Amazon.com Inc.'),
    ('META', 'Meta Platforms Inc.'),
    ('NVDA', 'NVIDIA Corporation'),
    ('NFLX', 'Netflix Inc.'),
    ('INTC', 'Intel Corporation'),
    ('AMD', 'Advanced Micro Devices Inc.'),
]

class Command(BaseCommand):
    help = 'Get 10 stocks into DB with real-time prices'

    def handle(self, *args, **options):
        for symbol, name in SEED_STOCKS:
            url = f"https://financialmodelingprep.com/api/v3/quote-short/{symbol}?apikey={FMP_API_KEY}"
            try:
                res = requests.get(url)
                data = res.json()
                price = data[0]['price'] if data else None
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Error fetching {symbol}: {e}'))
                price = None

            obj, created = Stock.objects.get_or_create(
                symbol=symbol,
                defaults={'company_name': name, 'last_price': price}
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'✅ Added: {symbol} - Price: {price}'))
            else:
                self.stdout.write(f'⚠️ Already exists: {symbol}')
