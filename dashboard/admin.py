from datetime import timedelta

from django.contrib import admin
from django.utils import timezone

from .models import MonthlyTarget


# ==========================================================
# WEEK FILTER
# ==========================================================

class WeekFilter(admin.SimpleListFilter):

    title = "Week"

    parameter_name = "week"

    def lookups(self, request, model_admin):

        return (

            ("this_week", "This Week"),

            ("last_week", "Last Week"),

        )

    def queryset(self, request, queryset):

        today = timezone.now().date()

        start_week = today - timedelta(days=today.weekday())

        end_week = start_week + timedelta(days=6)

        if self.value() == "this_week":

            return queryset.filter(

                created_at__date__range=(

                    start_week,

                    end_week,

                )

            )

        if self.value() == "last_week":

            last_start = start_week - timedelta(days=7)

            last_end = start_week - timedelta(days=1)

            return queryset.filter(

                created_at__date__range=(

                    last_start,

                    last_end,

                )

            )

        return queryset


# ==========================================================
# MONTHLY TARGET ADMIN
# ==========================================================

@admin.register(MonthlyTarget)
class MonthlyTargetAdmin(admin.ModelAdmin):

    list_display = (

        "month",

        "year",

        "revenue_target",

        "expense_budget",

        "profit_target",

        "created_at",

    )

    list_display_links = (

        "month",

        "year",

    )

    list_editable = (

        "revenue_target",

        "expense_budget",

        "profit_target",

    )

    search_fields = (

        "month",

        "year",

    )

    list_filter = (

        "month",

        "year",

        WeekFilter,

    )

    ordering = (

        "-created_at",

    )

    date_hierarchy = "created_at"

    list_per_page = 10

    save_on_top = True

    save_as = True

    empty_value_display = "-"

    readonly_fields = (

        "created_at",

        "updated_at",

    )

    fieldsets = (

        (

            "Monthly Information",

            {

                "fields": (

                    "month",

                    "year",

                ),

                "description":

                "Select the financial target month and year.",

            },

        ),

        (

            "Financial Targets",

            {

                "fields": (

                    "revenue_target",

                    "expense_budget",

                    "profit_target",

                ),

                "description":

                "Configure monthly financial targets.",

            },

        ),

        (

            "System Information",

            {

                "fields": (

                    "created_at",

                    "updated_at",

                ),

                "classes": (

                    "collapse",

                ),

            },

        ),

    )