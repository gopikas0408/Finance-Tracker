from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):

    # ==================================================
    # LIST DISPLAY
    # ==================================================

    list_display = (

        "transaction_id",

        "source_module",

        "transaction_type",

        "reference",

        "amount",

        "payment_mode",

        "status",

        "transaction_date",

        "created_by",

        "created_at",

    )

    # ==================================================
    # FILTER
    # ==================================================

    list_filter = (

        "source_module",

        "transaction_type",

        "payment_mode",

        "status",

        "transaction_date",

        "created_at",

    )

    # ==================================================
    # SEARCH
    # ==================================================

    search_fields = (

        "transaction_id",

        "reference",

        "notes",

        "created_by__username",

    )

    # ==================================================
    # ORDERING
    # ==================================================

    ordering = (

        "-created_at",

    )

    # ==================================================
    # READ ONLY FIELDS
    # ==================================================

    readonly_fields = (

        "transaction_id",

        "reference_id",

        "created_at",

        "updated_at",

    )

    # ==================================================
    # PAGINATION
    # ==================================================

    list_per_page = 20

    # ==================================================
    # DATE HIERARCHY
    # ==================================================

    date_hierarchy = "transaction_date"

    # ==================================================
    # FIELDSETS
    # ==================================================

    fieldsets = (

        (

            "Transaction Information",

            {

                "fields": (

                    "transaction_id",

                    "source_module",

                    "transaction_type",

                    "reference",

                    "reference_id",

                    "amount",

                    "payment_mode",

                    "transaction_date",

                    "status",

                    "notes",

                )

            },

        ),

        (

            "Audit Information",

            {

                "fields": (

                    "created_by",

                    "created_at",

                    "updated_at",

                )

            },

        ),

    )