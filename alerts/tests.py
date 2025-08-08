from django.test import TestCase, override_settings
from alerts.models import Alert
from stocks.models import Stock
from django.contrib.auth.models import User
from alerts.tasks import check_alerts
from django.utils import timezone
from datetime import timedelta
from django.core import mail




@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class AlertTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", email="test@gmail.com")
        self.stock = Stock.objects.create(symbol="AAPL", last_price=200, updated_at=timezone.now())
        
    def create_alert(self, condition, target_price, duration_minutes=None):
        return Alert.objects.create(
            user=self.user,
            stock=self.stock,
            condition=condition,
            target_price=target_price,
            duration_minutes=duration_minutes,
            is_active=True,
            triggered=False
        )

    # Test Cases for Immediate Alerts (without duration)
    def test_gt_alert_triggers_when_condition_met(self):
        alert = self.create_alert('gt', 150)
        check_alerts()
        alert.refresh_from_db()
        self.assertTrue(alert.triggered)  # 200 > 150 should trigger

    def test_lt_alert_triggers_when_condition_met(self):
        self.stock.last_price = 100  # Set price below target
        self.stock.save()
        alert = self.create_alert('lt', 150)
        check_alerts()
        alert.refresh_from_db()
        self.assertTrue(alert.triggered)  # 100 < 150 should trigger

    def test_gt_alert_does_not_trigger_below_target(self):
        self.stock.last_price = 100  # Set price below target
        self.stock.save()
        alert = self.create_alert('gt', 150)
        check_alerts()
        alert.refresh_from_db()
        self.assertFalse(alert.triggered)  # 100 > 150 is False

    # Test Cases for Duration Alerts
    def test_duration_alert_triggers_after_period(self):
        alert = self.create_alert('gt', 150, duration_minutes=30)
        
        # Simulate condition being met for required duration
        alert.first_triggered_at = timezone.now() - timedelta(minutes=31)
        alert.save()
        
        check_alerts()
        alert.refresh_from_db()
        self.assertTrue(alert.triggered)

    def test_duration_alert_does_not_trigger_prematurely(self):
        alert = self.create_alert('gt', 150, duration_minutes=30)
        
        # Simulate condition just met (not enough duration)
        alert.first_triggered_at = timezone.now() - timedelta(minutes=29)
        alert.save()
        
        check_alerts()
        alert.refresh_from_db()
        self.assertFalse(alert.triggered)

    def test_duration_alert_resets_when_condition_broken(self):
        alert = self.create_alert('gt', 150, duration_minutes=30)
        
        # Simulate condition was met for 15 minutes
        alert.first_triggered_at = timezone.now() - timedelta(minutes=15)
        alert.save()
        
        # Now break the condition
        self.stock.last_price = 100  # Set price below target
        self.stock.save()
        
        check_alerts()
        print('test_duration_alert_resets_when_condition_broken LAST')
        alert.refresh_from_db()
        self.assertIsNone(alert.first_triggered_at)  # Should reset
        self.assertFalse(alert.triggered)

    # Edge Cases
    def test_inactive_alert_does_not_trigger(self):
        alert = self.create_alert('gt', 150)
        alert.is_active = False
        alert.save()
        
        check_alerts()
        print('test_inactive_alert_does_not_trigger')
        alert.refresh_from_db()
        self.assertFalse(alert.triggered)

    def test_already_triggered_alert_does_not_retrigger(self):
        alert = self.create_alert('gt', 150)
        alert.triggered = True
        alert.save()
        
        check_alerts()
        print('test_already_triggered_alert_does_not_retrigger')
        alert.refresh_from_db()
        self.assertTrue(alert.triggered)  # Should remain triggered
        
        
    def test_email_sent_when_alert_triggers(self):
        alert = self.create_alert('lt', 250)
        self.stock.last_price = 200
        self.stock.save()

        check_alerts()

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Stock", mail.outbox[0].subject)
