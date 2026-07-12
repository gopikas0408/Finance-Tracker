from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
import re

from .models import Transaction


class TransactionForm(forms.ModelForm):

    class Meta:

        model = Transaction

        exclude = (

            "transaction_id",

            "reference_id",

            "created_by",

            "created_at",

            "updated_at",

        )

        widgets = {

            "source_module": forms.Select(attrs={
                "class": "form-select",
            }),

            "transaction_type": forms.Select(attrs={
                "class": "form-select",
            }),

            "reference": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Reference",
                "maxlength": "150",
            }),

            "amount": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "0.00",
                "min": "1",
                "step": "0.01",
            }),

            "payment_mode": forms.Select(attrs={
                "class": "form-select",
            }),

            "transaction_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date",
            }),

            "status": forms.Select(attrs={
                "class": "form-select",
            }),

            "notes": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Enter Notes (Optional)",
                "maxlength": "500",
            }),

        }

    # ==========================================
    # Reference Validation
    # ==========================================

    def clean_reference(self):

        reference = self.cleaned_data.get("reference")

        if not reference:

            raise ValidationError(

                "Reference is required."

            )

        reference = reference.strip()

        if len(reference) < 3:

            raise ValidationError(

                "Reference must contain at least 3 characters."

            )

        if len(reference) > 150:

            raise ValidationError(

                "Reference cannot exceed 150 characters."

            )

        if not re.match(

            r"^[A-Za-z0-9\s\-_/().,&]+$",

            reference

        ):

            raise ValidationError(

                "Reference contains invalid characters."

            )

        return reference

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

                "Amount exceeds the allowed limit."

            )

        return amount

    # ==========================================
    # Transaction Date Validation
    # ==========================================

    def clean_transaction_date(self):

        transaction_date = self.cleaned_data.get(

            "transaction_date"

        )

        if not transaction_date:

            raise ValidationError(

                "Transaction date is required."

            )

        if transaction_date > timezone.now().date():

            raise ValidationError(

                "Future transaction dates are not allowed."

            )

        return transaction_date

    # ==========================================
    # Notes Validation
    # ==========================================

    def clean_notes(self):

        notes = self.cleaned_data.get("notes")

        if notes:

            notes = notes.strip()

            if len(notes) < 5:

                raise ValidationError(

                    "Notes must contain at least 5 characters."

                )

            if len(notes) > 500:

                raise ValidationError(

                    "Notes cannot exceed 500 characters."

                )

        return notes

    # ==========================================
    # Form Validation
    # ==========================================

    def clean(self):

        cleaned_data = super().clean()

        status = cleaned_data.get("status")

        amount = cleaned_data.get("amount")

        if (

            status == "Completed"

            and

            amount is not None

            and

            amount <= 0

        ):

            raise ValidationError(

                "Completed transactions must have an amount greater than zero."

            )

        return cleaned_data