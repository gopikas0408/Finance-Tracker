from django.db import models
from django.core.validators import (
    MinValueValidator,
    FileExtensionValidator,
)
from django.core.exceptions import ValidationError
from django.utils import timezone

from core.models import BaseModel


class IncomeSource(BaseModel):

    source_name = models.CharField(
        max_length=100,
        unique=True
    )

    status = models.BooleanField(
        default=True
    )

    class Meta:
        verbose_name = "Income Source"
        verbose_name_plural = "Income Sources"
        ordering = ["source_name"]

    def __str__(self):
        return self.source_name


class Income(BaseModel):

    PAYMENT_MODE = [
        ("Cash", "Cash"),
        ("UPI", "UPI"),
        ("Bank", "Bank Transfer"),
        ("Card", "Card"),
        ("Cheque", "Cheque"),
    ]

    income_source = models.ForeignKey(
        IncomeSource,
        on_delete=models.CASCADE,
        related_name="incomes"
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[
            MinValueValidator(
                1,
                message="Amount must be greater than zero."
            )
        ]
    )

    payment_mode = models.CharField(
        max_length=20,
        choices=PAYMENT_MODE,
        default="Cash"
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    attachment = models.FileField(
        upload_to="income/",
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    "pdf",
                    "jpg",
                    "jpeg",
                    "png"
                ]
            )
        ]
    )

    received_date = models.DateField()

    class Meta:
        verbose_name = "Income"
        verbose_name_plural = "Income"
        ordering = [
            "-received_date",
            "-created_at"
        ]

    def clean(self):

        super().clean()

        # Amount Validation
        if self.amount is not None and self.amount <= 0:
            raise ValidationError({
                "amount": "Amount must be greater than zero."
            })

        # Future Date Validation
        if self.received_date and self.received_date > timezone.localdate():
            raise ValidationError({
                "received_date": "Future dates are not allowed."
            })

        # Description Validation
        if self.description:

            self.description = self.description.strip()

            if len(self.description) < 5:
                raise ValidationError({
                    "description": "Description should contain at least 5 characters."
                })

    def __str__(self):
        return f"{self.income_source} - ₹{self.amount}"