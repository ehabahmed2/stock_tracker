from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Alert
from django.core.mail import send_mail
from decouple import config


@shared_task
def check_alerts():
    print("## المهمة بدأت ##") 
    now = timezone.now()
    alerts = Alert.objects.filter(is_active=True, triggered=False)
    
    for alert in alerts:
        stock = alert.stock
        current_price = stock.last_price
        
        # Skip if stock price hasn't been updated
        if not stock.updated_at:
            continue
            
        condition_met = False
        
        # Check conditions
        if alert.condition == 'gt' and current_price > alert.target_price:
            condition_met = True
        elif alert.condition == 'lt' and current_price < alert.target_price:
            condition_met = True
            
        # If condition is met, check duration if specified
        if condition_met:
            if alert.duration_minutes:
                # Verify price has stayed beyond threshold for required duration
                if stock.updated_at <= now - timedelta(minutes=alert.duration_minutes):
                    send_alert(alert, current_price)
            else:
                # No duration requirement - trigger immediately
                send_alert(alert, current_price)


def send_alert(alert, current_price):
    user_email = alert.user.email
    stock_symbol = alert.stock.symbol
    condition = ">" if alert.condition == "gt" else "<"

    message = f"Stock {stock_symbol} is now {condition} {alert.target_price} (Current: {current_price})"

    # Print to console
    print(f"🔔 ALERT: {message}")

    # Optional: send email
    if user_email:
        send_mail(
            subject='Stock Price Alert',
            message=message,
            from_email= config('EMAIL_HOST_USER'),
            recipient_list=[user_email],
            fail_silently=False,
        )

    alert.triggered = True
    alert.save()









