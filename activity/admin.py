from django.contrib import admin

from .models import (
    Notification,
    ActivityLog,
    Reminder,
    MonthlyTarget,
)


# =====================================================
# NOTIFICATION
# =====================================================

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "module",
        "action",
        "priority",
        "is_read",
        "created_by",
        "created_at",
    )

    list_filter = (
        "module",
        "action",
        "priority",
        "is_read",
    )

    search_fields = (
        "title",
        "message",
    )

    ordering = (
        "-created_at",
    )


# =====================================================
# ACTIVITY LOG
# =====================================================

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):

    list_display = (
        "module",
        "action",
        "record_name",
        "user",
        "created_at",
    )

    list_filter = (
        "module",
        "action",
    )

    search_fields = (
        "record_name",
        "description",
    )

    ordering = (
        "-created_at",
    )


# =====================================================
# REMINDER
# =====================================================

@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "module",
        "priority",
        "reminder_date",
        "status",
        "created_by",
        "created_at",
    )

    list_filter = (
        "status",
        "priority",
        "module",
        "reminder_date",
    )

    search_fields = (
        "title",
        "message",
    )

    ordering = (
        "-reminder_date",
    )

# =====================================================
# MONTHLY TARGET
# =====================================================

@admin.register(MonthlyTarget)
class MonthlyTargetAdmin(admin.ModelAdmin):

    list_display = (
        "month",
        "year",
        "income_target",
        "expense_limit",
        "profit_target",
    )

    ordering = (
        "-year",
        "-id",
    )