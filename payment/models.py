from django.db import models
from django.conf import settings
from product.models import Order

class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reference = models.CharField(max_length=100, unique=True)  # Paystack transaction reference
    status = models.CharField(max_length=20, default='pending')  # pending, success, failed
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Payment for {self.order} - {self.status}'
