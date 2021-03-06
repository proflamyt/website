# stdlib import

# django imports
from django.conf import settings
from django.db import models

# 3rd party imports

# project imports


class PaymentTypeModel(models.Model):
    """Represents either a Plan or OnceOff payment type"""
    EXPIRY = (
        (30, 'Month'),
        (120, 'Quater'),
        (365, 'Year'),
    )

    description = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(decimal_places=2, max_digits=9)
    payment_plan = models.PositiveIntegerField(unique=True, blank=True, null=True)
    currency = models.CharField(max_length=3, default="USD")
    custom_logo = models.URLField(max_length=500, blank=True, null=True)
    custom_title = models.CharField(max_length=200, blank=True, null=True)
    pay_button_text = models.CharField(max_length=100, default="Sign Up")
    payment_options = models.CharField(max_length=100, default="card")
    created_datetime = models.DateTimeField(auto_now_add=True)
    expiry = models.IntegerField(choices=EXPIRY ,default=30)

    class Meta:
        verbose_name = "Payment Type"

    def __str__(self):
        return self.description


class TransactionModel(models.Model):
    """Represents a transaction for a specific payment type and user"""

    payment_type = models.ForeignKey(
        to=PaymentTypeModel, related_name="transactions", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        related_name="transactions",
        on_delete=models.CASCADE,
    )
    created_datetime = models.DateTimeField(auto_now_add=True)
    reference = models.CharField(max_length=200)
    flutterwave_reference = models.CharField(max_length=200)
    order_reference = models.CharField(max_length=200)
    amount = models.DecimalField(decimal_places=2, max_digits=9)
    charged_amount = models.DecimalField(decimal_places=2, max_digits=9)
    status = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Transaction"

    def __str__(self):
        return self.reference
