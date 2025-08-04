from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from alerts.models import Alert
from django.core.mail import send_mail


def send_alert(alert, current_price):
    print(f'this is an alert for {alert} and current price is: {current_price}')

@shared_task
def check_alerts():
    now = timezone.now()
    alerts = Alert.objects.filter(is_active=True, triggered=False)
    
    # now go through all active alerts
    for alert in alerts:
        stock = alert.stock
        current_price = stock.last_price
        
        # check current condition and if greater than targer then target then send emails
        if alert.condition == 'gt' and current_price > alert.target_price:
            # check if there is duration minutes, if there is then wait 
            if alert.duration_minutes:
                # check if last update is older than time specified by the user (last update - now minus 20 mins for example)
                if stock.updated_at < now - timedelta(minutes=alert.duration_minutes):
                    send_alert(alert, current_price)
            else:
                send_alert(alert, current_price)

        # same thing but for less than
        elif alert.condition == 'lt' and current_price < alert.target_price:
            if stock.updated_at < now - timedelta(minutes=alert.duration_minutes):
                    send_alert(alert, current_price)
            else:
                send_alert(alert, current_price)
    




# def s_email(alert, current_price):
#     user_email = alert.user.email
#     stock_symbol = alert.stock.symbol
#     condition = ">" if alert.condition == "gt" else "<"

#     message = f"Stock {stock_symbol} is now {condition} {alert.target_price} (Current: {current_price})"

#     # Print to console
#     print(f"🔔 ALERT: {message}")

#     # Optional: send email
#     if user_email:
#         send_mail(
#             subject='Stock Price Alert',
#             message=message,
#             from_email='your_email@gmail.com',
#             recipient_list=[user_email],
#             fail_silently=True,
#         )

#     alert.triggered = True
#     alert.save()









