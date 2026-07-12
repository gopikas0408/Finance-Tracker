from django.contrib import admin
from .models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):

    list_display = (
        "expense_name",
        "category",
        "amount",
        "payment_mode",
        "expense_date",
        "created_at",
    )

    list_filter = (
        "category",
        "payment_mode",
        "expense_date",
    )

    search_fields = (
        "expense_name",
        "category",
    )

    ordering = (
        "-id",
    )