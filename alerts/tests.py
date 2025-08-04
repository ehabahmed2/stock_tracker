
from django.test import TestCase
from alerts.models import Alert
from stocks.models import Stock
from django.contrib.auth.models import User
from alerts.tasks import check_alerts

class AlertTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", email="test@gmail.com")
        self.stock = Stock.objects.create(symbol="AAPL", last_price=200)
        self.alert = Alert.objects.create(
            user=self.user,
            stock=self.stock,
            condition='gt',
            target_price=150,
            is_active=True,
            triggered=False
        )

    def test_alert_triggers_when_condition_met(self):
        check_alerts()
        self.alert.refresh_from_db()
        self.assertTrue(self.alert.triggered)
