from django.contrib import admin
from alerts.models import Alert
from stocks.models import Stock
# Register your models here.
admin.site.register(Alert)
admin.site.register(Stock)