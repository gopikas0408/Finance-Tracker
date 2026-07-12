from .models import (
    Notification,
    ActivityLog,
    Reminder,
    MonthlyTarget,
)


# =====================================================
# CREATE NOTIFICATION
# =====================================================

def create_notification(

    title,

    message,

    module,

    action,

    priority="Medium",

    user=None,

):

    Notification.objects.create(

        title=title,

        message=message,

        module=module,

        action=action,

        priority=priority,

        created_by=user,

    )


# =====================================================
# CREATE ACTIVITY LOG
# =====================================================

def log_activity(

    module,

    action,

    record_name,

    description,

    user=None,

):

    ActivityLog.objects.create(

        module=module,

        action=action,

        record_name=record_name,

        description=description,

        user=user,

    )


# =====================================================
# CREATE REMINDER
# =====================================================

def create_reminder(

    title,

    message,

    reminder_date,

    user=None,

):

    Reminder.objects.create(

        title=title,

        message=message,

        reminder_date=reminder_date,

        created_by=user,

    )


# =====================================================
# TARGET CHECK
# =====================================================

def check_target(

    current_income,

    current_expense,

    month_target,

    user=None,

):

    if current_income >= month_target.income_target:

        create_notification(

            title="🎯 Income Target Achieved",

            message=f"Congratulations! Monthly income target ₹{month_target.income_target} achieved.",

            module="Dashboard",

            action="Achievement",

            priority="High",

            user=user,

        )

    if current_expense > month_target.expense_limit:

        create_notification(

            title="⚠ Expense Limit Crossed",

            message=f"Monthly expense exceeded ₹{month_target.expense_limit}.",

            module="Dashboard",

            action="Reminder",

            priority="Critical",

            user=user,

        )