from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Alert
from django.core.mail import send_mail
from decouple import config


@shared_task
def check_alerts():
    print("## started mission  :D ##") 
    now = timezone.now()
    alerts = Alert.objects.filter(is_active=True, triggered=False)
    
    for alert in alerts:
        stock = alert.stock
        current_price = float(stock.last_price) if stock.last_price is not None else None
        target_price = float(alert.target_price)
        
        # Skip if stock price hasn't been updated
        if not stock.updated_at:
            continue
            
        # Check conditions
        condition_met = (
            (alert.condition == 'gt' and current_price > target_price) or
            (alert.condition == 'lt' and current_price < target_price)
        )
            
        # Handle duration alerts
        if alert.duration_minutes:
            if condition_met:
                if not alert.first_triggered_at:
                    # First time condition is met - record timestamp
                    alert.first_triggered_at = now
                    alert.save(update_fields=['first_triggered_at'])
                else:
                    # Check if duration requirement is satisfied
                    duration_met = (now - alert.first_triggered_at) >= timedelta(minutes=alert.duration_minutes)
                    if duration_met:
                        send_alert(alert, current_price)

            else:
                # Condition not met - reset tracking
                if alert.first_triggered_at:
                    alert.first_triggered_at = None
                    alert.save(update_fields=['first_triggered_at'])
        else:
            # Immediate trigger for non-duration alerts
            if condition_met:
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
    # disable this alert
    alert.is_active = False









