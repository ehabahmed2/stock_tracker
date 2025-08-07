from django.db import models
from django.contrib.auth.models import User
from stocks.models import Stock

class Alert(models.Model):
    CONDITION_CHOICES = (
        ('gt', 'Greater than'),
        ('lt', 'Less than'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    condition = models.CharField(max_length=2, choices=CONDITION_CHOICES)
    
    target_price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    triggered = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    first_triggered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} alert for {self.stock.symbol}"
