from django import forms
from .models import Income
import os
from django.utils import timezone


class IncomeForm(forms.ModelForm):

    class Meta:
        model = Income
        fields = "__all__"

        widgets = {

            "received_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control"
                }
            ),

            "income_source": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "1",
                    "step": "0.01"
                }
            ),

            "payment_mode": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "maxlength": "500"
                }
            ),

            "attachment": forms.FileInput(
                attrs={
                    "class": "form-control",
                    "accept": ".pdf,.jpg,.jpeg,.png"
                }
            )

        }

    # -------------------------------
    # Amount Validation
    # -------------------------------

    def clean_amount(self):
        amount = self.cleaned_data.get("amount")

        if amount is None:
            raise forms.ValidationError("Amount is required.")

        if amount <= 0:
            raise forms.ValidationError("Amount must be greater than zero.")

        return amount

    # -------------------------------
    # Description Validation
    # -------------------------------

    def clean_description(self):
        description = self.cleaned_data.get("description")

        if description:
            description = description.strip()

            if len(description) < 5:
                raise forms.ValidationError(
                    "Description should contain at least 5 characters."
                )

        return description

    # -------------------------------
    # Attachment Validation
    # -------------------------------

    def clean_attachment(self):
        attachment = self.cleaned_data.get("attachment")

        if attachment:

            ext = os.path.splitext(attachment.name)[1].lower()

            allowed = [".pdf", ".jpg", ".jpeg", ".png"]

            if ext not in allowed:
                raise forms.ValidationError(
                    "Only PDF, JPG, JPEG and PNG files are allowed."
                )

            if attachment.size > 5 * 1024 * 1024:
                raise forms.ValidationError(
                    "File size must be less than 5 MB."
                )

        return attachment
    
    # -------------------------------
# Received Date Validation
# -------------------------------

def clean_received_date(self):

    received_date = self.cleaned_data.get("received_date")

    if not received_date:

        raise forms.ValidationError(
            "Received Date is required."
        )

    if received_date > timezone.localdate():

        raise forms.ValidationError(
            "Future dates are not allowed."
        )

    return received_date