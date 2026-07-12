from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
import os

from .models import Expense


class ExpenseForm(forms.ModelForm):

    class Meta:

        model = Expense

        fields = "__all__"

        widgets = {

            "expense_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Expense Name"
                }
            ),

            "category": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Amount",
                    "min": "1",
                    "step": "0.01"
                }
            ),

            "payment_mode": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "expense_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Enter Description"
                }
            ),

            "attachment": forms.ClearableFileInput(
                attrs={
                    "class": "form-control"
                }
            ),

        }

    # ==========================================
    # Expense Name Validation
    # ==========================================

    def clean_expense_name(self):

        expense_name = self.cleaned_data.get("expense_name", "").strip()

        if not expense_name:
            raise ValidationError("Expense Name is required.")

        if len(expense_name) < 3:
            raise ValidationError(
                "Expense Name must contain at least 3 characters."
            )

        if len(expense_name) > 100:
            raise ValidationError(
                "Expense Name cannot exceed 100 characters."
            )

        return expense_name

    # ==========================================
    # Category Validation
    # ==========================================

    def clean_category(self):

        category = self.cleaned_data.get("category")

        if not category:
            raise ValidationError(
                "Please select an Expense Category."
            )

        return category

    # ==========================================
    # Amount Validation
    # ==========================================

    def clean_amount(self):

        amount = self.cleaned_data.get("amount")

        if amount is None:
            raise ValidationError(
                "Amount is required."
            )

        if amount <= 0:
            raise ValidationError(
                "Amount must be greater than zero."
            )

        if amount > 999999999:
            raise ValidationError(
                "Amount is too large."
            )

        return amount

    # ==========================================
    # Payment Mode Validation
    # ==========================================

    def clean_payment_mode(self):

        payment_mode = self.cleaned_data.get("payment_mode")

        if not payment_mode:
            raise ValidationError(
                "Please select Payment Mode."
            )

        return payment_mode

    # ==========================================
    # Expense Date Validation
    # ==========================================

    def clean_expense_date(self):

        expense_date = self.cleaned_data.get("expense_date")

        if not expense_date:
            raise ValidationError(
                "Expense Date is required."
            )

        if expense_date > timezone.localdate():
            raise ValidationError(
                "Future dates are not allowed."
            )

        return expense_date

    # ==========================================
    # Description Validation
    # ==========================================

    def clean_description(self):

        description = self.cleaned_data.get("description")

        if description:

            description = description.strip()

            if len(description) < 5:
                raise ValidationError(
                    "Description must contain at least 5 characters."
                )

            if len(description) > 500:
                raise ValidationError(
                    "Description cannot exceed 500 characters."
                )

        return description

    # ==========================================
    # Attachment Validation
    # ==========================================

    def clean_attachment(self):

        attachment = self.cleaned_data.get("attachment")

        if attachment:

            allowed_extensions = [
                ".pdf",
                ".jpg",
                ".jpeg",
                ".png"
            ]

            extension = os.path.splitext(
                attachment.name
            )[1].lower()

            if extension not in allowed_extensions:

                raise ValidationError(
                    "Only PDF, JPG, JPEG and PNG files are allowed."
                )

            if attachment.size > 5 * 1024 * 1024:

                raise ValidationError(
                    "Maximum file size is 5 MB."
                )

        return attachment