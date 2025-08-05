import os
from celery import Celery
from celery.schedules import crontab  # this for scheduling



# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stock_mgmnt.settings')

app = Celery('stock_mgmnt')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
    



# to run checks 
app.conf.beat_schedule = {
    'fetch-stocks-every-minute': {
        'task': 'stocks.tasks.fetch_stock_prices',
        'schedule': crontab(minute='*/5'),
    },
    'check-alerts-every-minute': {
        'task': 'alerts.tasks.check_alerts',
        'schedule': crontab(minute='*/5'),
    },
}