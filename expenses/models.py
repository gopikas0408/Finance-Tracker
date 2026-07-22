from xml.parsers.expat import errors

from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
import os


class Expense(models.Model):

    PAYMENT_CHOICES = [

        ("Cash", "Cash"),
        ("UPI", "UPI"),
        ("Bank", "Bank Transfer"),
        ("Card", "Card"),
        ("Cheque", "Cheque"),

    ]

    CATEGORY_CHOICES = [

        ("Office", "Office"),
        ("Salary", "Salary"),
        ("Marketing", "Marketing"),
        ("Travel", "Travel"),
        ("Food", "Food"),
        ("Software", "Software"),
        ("Utilities", "Utilities"),
        ("Others", "Others"),

    ]

    expense_name = models.CharField(
        max_length=150
    )

    category = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    payment_mode = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES
    )
    
   

    # ===========================
    # ONLINE PAYMENT
    # ===========================

    transaction_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    # ===========================
    # CHEQUE DETAILS
    # ===========================

    cheque_number = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    bank_name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    expense_date = models.DateField()

    description = models.TextField(
        blank=True,
        null=True
    )

    attachment = models.FileField(
        upload_to="expenses/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = ["-id"]

        verbose_name = "Expense"

        verbose_name_plural = "Expenses"

    def __str__(self):

        return self.expense_name

    # ======================================
    # Model Validation
    # ======================================

    def clean(self):

        errors = {}

        # Expense Name
        if not self.expense_name:
            errors["expense_name"] = "Expense Name is required."

        elif len(self.expense_name.strip()) < 3:
            errors["expense_name"] = "Expense Name must contain at least 3 characters."

        elif len(self.expense_name.strip()) > 150:
            errors["expense_name"] = "Expense Name cannot exceed 150 characters."

        # Amount
        if self.amount is None:
            errors["amount"] = "Amount is required."

        elif self.amount <= 0:
            errors["amount"] = "Amount must be greater than zero."

        elif self.amount > 999999999:
            errors["amount"] = "Amount is too large."

        # Expense Date
        if self.expense_date:

            if self.expense_date > timezone.localdate():
                errors["expense_date"] = "Future dates are not allowed."

        # Description
        if self.description:

            description = self.description.strip()

            if len(description) < 5:
                errors["description"] = "Description must contain at least 5 characters."

            elif len(description) > 500:
                errors["description"] = "Description cannot exceed 500 characters."

        # Attachment
        if self.attachment:

            extension = os.path.splitext(
                self.attachment.name
            )[1].lower()

            allowed_extensions = [
                ".pdf",
                ".jpg",
                ".jpeg",
                ".png"
            ]

            if extension not in allowed_extensions:
                errors["attachment"] = "Only PDF, JPG, JPEG and PNG files are allowed."

            if self.attachment.size > 5 * 1024 * 1024:
                errors["attachment"] = "Maximum file size is 5 MB."

        if errors:
            raise ValidationError(errors)
        
        
        

    # ======================================
    # Save Validation
    # ======================================

    def save(self, *args, **kwargs):

        self.full_clean()

        super().save(*args, **kwargs)
        
    
        
class CashDenomination(models.Model):

    DENOMINATION_CHOICES = [

        
        (500, "₹500"),
        (200, "₹200"),
        (100, "₹100"),
        (50, "₹50"),
        (20, "₹20"),
        (10, "₹10"),

    ]

    expense = models.ForeignKey(
        Expense,
        on_delete=models.CASCADE,
        related_name="cash_denominations",
    )

    denomination = models.IntegerField(
        choices=DENOMINATION_CHOICES
    )

    notes_count = models.PositiveIntegerField()

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    class Meta:
        ordering = ["id"]

    def save(self, *args, **kwargs):

        self.amount = self.denomination * self.notes_count

        super().save(*args, **kwargs)

    def __str__(self):

        return f"{self.denomination} x {self.notes_count}"