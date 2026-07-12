from django.contrib import admin
from .models import IncomeSource, Income


@admin.register(IncomeSource)
class IncomeSourceAdmin(admin.ModelAdmin):

    list_display = (
        'source_name',
        'status',
        'created_at',
    )

    search_fields = (
        'source_name',
    )


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):

    list_display = (
        'income_source',
        'amount',
        'payment_mode',
        'received_date',
    )

    list_filter = (
        'payment_mode',
        'received_date',
    )

    search_fields = (
        'income_source__source_name',
    )