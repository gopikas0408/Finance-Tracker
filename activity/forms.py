from django import forms

from .models import (
    MonthlyTarget,
    Reminder,
)


class MonthlyTargetForm(forms.ModelForm):

    class Meta:

        model = MonthlyTarget

        fields = "__all__"

        widgets = {

            "month": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "year": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "income_target": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "expense_limit": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "profit_target": forms.NumberInput(attrs={
                "class": "form-control"
            }),

        }


class ReminderForm(forms.ModelForm):

    class Meta:

        model = Reminder

        fields = "__all__"

        widgets = {

            "title": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "message": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
            }),

            "module": forms.Select(attrs={
                "class": "form-select"
            }),

            "priority": forms.Select(attrs={
                "class": "form-select"
            }),

            "reminder_date": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control",
            }),

            "status": forms.Select(attrs={
                "class": "form-select"
            }),

            "created_by": forms.Select(attrs={
                "class": "form-select"
            }),

        }