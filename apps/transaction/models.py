# Python
import uuid

# Django
from django.db import models


# Create your models here.
class Transaction(models.Model):
    """Model Transaction"""

    class StateChoices(models.TextChoices):
        CLOSED = "closed", "Transacción cobrada"
        REVERSED = "reversed", "Cobro realizado y regresado (para validar tarjeta)"
        PENDING = "pending", "pendiente de cobrar"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    company = models.ForeignKey(
        "company.Company",
        on_delete=models.PROTECT,
        verbose_name="Company",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Price",
    )
    transaction_date = models.DateTimeField(
        null=True, verbose_name="Fecha de transacción"
    )
    transaction_state = models.CharField(
        max_length=16,
        null=True,
        choices=StateChoices.choices,
        verbose_name="Estado de transacción",
    )
    approval_state = models.BooleanField(
        default=False, verbose_name="Estado de aprobación"
    )
    payment_state = models.BooleanField(
        default=False,
        verbose_name="Cobro Final",
    )

    class Meta:
        """Class information"""

        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ["transaction_date"]

    def __str__(self):
        return f"{self.company}"

    def save(self, *args, **kwargs):
        """Overwrite method save for change payment_state (Cobro final)"""
        if self.transaction_state == "closed" and self.approval_state:
            self.payment_state = True
        super(Transaction, self).save(*args, **kwargs)
