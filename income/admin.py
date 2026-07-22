from django.contrib import admin
from .models import IncomeSource, Income, CashDenomination


@admin.register(IncomeSource)
class IncomeSourceAdmin(admin.ModelAdmin):

    list_display = (
        "source_name",
        "status",
        "created_at",
    )

    search_fields = (
        "source_name",
    )


# ==============================
# CASH DENOMINATION INLINE
# ==============================

class CashDenominationInline(admin.TabularInline):

    model = CashDenomination

    extra = 1

    fields = (
        "denomination",
        
        "notes_count",
        "amount",
    )

    readonly_fields = (
        "amount",
    )


# ==============================
# INCOME ADMIN
# ==============================

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):

    list_display = (
        "income_source",
        "amount",
        "payment_mode",
        "received_date",
    )

    list_filter = (
        "payment_mode",
        "received_date",
    )

    search_fields = (
        "income_source__source_name",
    )

    inlines = [
        CashDenominationInline,
    ]