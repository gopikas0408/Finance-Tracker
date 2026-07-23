from django import forms
from django.forms import inlineformset_factory
from django.utils import timezone
import os

from .models import (
    Income,
    CashDenomination,
)


class IncomeForm(forms.ModelForm):

    class Meta:
        model = Income
        fields = (
            "income_source",
            "amount",
            "payment_mode",
            "transaction_id",
            "cheque_number",
            "bank_name",
            "received_date",
            "description",
            "attachment",
        )

        widgets = {

            "received_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),

            "income_source": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "transaction_id": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "cheque_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "bank_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "readonly": True,
                }
            ),

            "payment_mode": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),

            "attachment": forms.FileInput(
                attrs={
                    "class": "form-control",
                    "accept": ".pdf,.jpg,.jpeg,.png",
                }
            ),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        
        

        if self.instance.pk:
            
            self.fields["income_source"].widget.attrs["disabled"] = True
            self.fields["payment_mode"].widget.attrs["disabled"] = True
            self.fields["amount"].widget.attrs["readonly"] = True

            self.fields["payment_mode"].widget.attrs["style"] = (
                "pointer-events:none;background:#f8f9fa;"
            )

            self.fields["received_date"].widget.attrs["readonly"] = True

            self.fields["transaction_id"].widget.attrs["readonly"] = True

            self.fields["cheque_number"].widget.attrs["readonly"] = True

            self.fields["bank_name"].widget.attrs["readonly"] = True

    def clean_amount(self):

        amount = self.cleaned_data.get("amount")

        if amount is None:

            raise forms.ValidationError(
                "Amount is required."
            )

        if amount <= 0:

            raise forms.ValidationError(
                "Amount must be greater than zero."
            )

        return amount

    def clean_received_date(self):

        received_date = self.cleaned_data.get("received_date")

        if received_date > timezone.localdate():

            raise forms.ValidationError(
                "Future dates are not allowed."
            )

        return received_date

    def clean_description(self):

        description = self.cleaned_data.get("description")

        if description:

            description = description.strip()

            if len(description) < 5:

                raise forms.ValidationError(
                    "Description should contain at least 5 characters."
                )

        return description

    def clean_attachment(self):

        attachment = self.cleaned_data.get("attachment")

        if attachment:

            ext = os.path.splitext(
                attachment.name
            )[1].lower()

            allowed = [
                ".pdf",
                ".jpg",
                ".jpeg",
                ".png",
            ]

            if ext not in allowed:

                raise forms.ValidationError(
                    "Only PDF, JPG, JPEG and PNG files are allowed."
                )

            if attachment.size > 5 * 1024 * 1024:

                raise forms.ValidationError(
                    "Maximum file size is 5 MB."
                )

        return attachment


class CashDenominationForm(forms.ModelForm):

    class Meta:

        model = CashDenomination

        fields = (
            "denomination",
            
            "notes_count",
        )

        widgets = {

            "denomination": forms.Select(
                attrs={
                    "class": "form-select denomination",
                }
            ),

            

            "notes_count": forms.NumberInput(
                attrs={
                    "class": "form-control notes-count",
                    "min": 1,
                }
            ),

        }

    def clean(self):

        cleaned_data = super().clean()

        denomination = cleaned_data.get("denomination")

        

        notes = cleaned_data.get("notes_count")

        if notes is None or notes <= 0:

            raise forms.ValidationError(
                "Notes count must be greater than zero."
            )

        value = int(denomination)

        cleaned_data["amount"] = value * notes

        return cleaned_data


CashDenominationFormSet = inlineformset_factory(
    Income,
    CashDenomination,
    form=CashDenominationForm,
    extra=1,
    can_delete=True,
)

IncomeCashDenominationEditFormSet = inlineformset_factory(
    Income,
    CashDenomination,
    form=CashDenominationForm,
    extra=0,
    can_delete=False
)