from django.db import models

# Create your models here.
class Stock(models.Model):
    symbol = models.CharField(max_length=30, unique=True)
    company_name = models.CharField(max_length=100)
    last_price = models.FloatField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.symbol} Price: {self.last_price}"
