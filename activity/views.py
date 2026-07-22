from django.utils import timezone

from django.shortcuts import render

from .models import (
    Notification,
    ActivityLog,
    Reminder,
    MonthlyTarget,
)
from django.db.models import Sum, Q
from transactions.models import Transaction
from .models import Achievement
from django.core.paginator import Paginator

def notification_center(request):

    context = {

        "notification_count": Notification.objects.count(),

        "activity_count": ActivityLog.objects.count(),

        "reminder_count": Reminder.objects.count(),

        "target_count": MonthlyTarget.objects.count(),

        "active_page": "activity",

    }

    return render(

        request,

        "activity/notification_center.html",

        context

    )


def notification_list(request):

    Notification.objects.filter(
        is_read=False
    ).update(is_read=True)

    notifications = Notification.objects.all().order_by("-created_at")

    # Summary Cards
    total_notifications = notifications.count()

    read_notifications = notifications.filter(
        is_read=True
    ).count()

    unread_notifications = notifications.filter(
        is_read=False
    ).count()

    paginator = Paginator(
        notifications,
        10
    )

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "activity/notification_list.html",
        {
            "notifications": page_obj,
            "page_obj": page_obj,
            "total_notifications": total_notifications,
            "read_notifications": read_notifications,
            "unread_notifications": unread_notifications,
            "active_page": "notifications",
            "active_activity": "notifications",
        }
    )


from django.db.models import Q

def activity_history(request):

    history = ActivityLog.objects.all().order_by("-created_at")

    # ==========================================
    # SEARCH
    # ==========================================

    search = request.GET.get("search")

    if search:

        history = history.filter(

            Q(module__icontains=search) |

            Q(action__icontains=search) |

            Q(record_name__icontains=search)

        )

    # ==========================================
    # SUMMARY CARDS
    # ==========================================

    total_activities = ActivityLog.objects.count()

    add_actions = ActivityLog.objects.filter(
        action="Add"
    ).count()

    edit_actions = ActivityLog.objects.filter(
        action="Edit"
    ).count()

    delete_actions = ActivityLog.objects.filter(
        action="Delete"
    ).count()

    # ==========================================
    # PAGINATION
    # ==========================================

    paginator = Paginator(history, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(

        request,

        "activity/activity_history.html",

        {

            "history": page_obj,

            "page_obj": page_obj,

            "search": search,

            "total_activities": total_activities,

            "add_actions": add_actions,

            "edit_actions": edit_actions,

            "delete_actions": delete_actions,

            "active_page": "history",

            "active_activity": "history",

        }

    )


def reminder_list(request):

    reminders = Reminder.objects.all().order_by("reminder_date")

    # ==========================================
    # SEARCH
    # ==========================================

    search = request.GET.get("search")

    if search:

        reminders = reminders.filter(

            Q(title__icontains=search) |

            Q(message__icontains=search)

        )

    # ==========================================
    # SUMMARY CARDS
    # ==========================================

    total_reminders = Reminder.objects.count()

    today_reminders = Reminder.objects.filter(
        reminder_date=timezone.localdate()
    ).count()

    completed_reminders = Reminder.objects.filter(
        status="Completed"
    ).count()

    pending_reminders = Reminder.objects.filter(
        status="Pending"
    ).count()

    # ==========================================
    # PAGINATION
    # ==========================================

    paginator = Paginator(reminders, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(

        request,

        "activity/reminder_list.html",

        {

            "reminders": page_obj,

            "page_obj": page_obj,

            "search": search,

            "total_reminders": total_reminders,

            "today_reminders": today_reminders,

            "completed_reminders": completed_reminders,

            "pending_reminders": pending_reminders,

            "active_page": "reminders",

            "active_activity": "reminders",

        }

    )




def target_list(request):

    # ==========================================
    # TARGETS
    # ==========================================

    targets = MonthlyTarget.objects.all().order_by("-year", "-id")

    # ==========================================
    # SUMMARY CARDS
    # ==========================================

    total_targets = targets.count()

    total_income_target = targets.aggregate(
        total=Sum("income_target")
    )["total"] or 0

    total_expense_limit = targets.aggregate(
        total=Sum("expense_limit")
    )["total"] or 0

    total_profit_target = targets.aggregate(
        total=Sum("profit_target")
    )["total"] or 0

    # ==========================================
    # CURRENT TRANSACTION VALUES
    # ==========================================

    current_income = Transaction.objects.filter(
        transaction_type="Income"
    ).aggregate(
        total=Sum("amount")
    )["total"] or 0

    current_expense = Transaction.objects.filter(
        transaction_type="Expense"
    ).aggregate(
        total=Sum("amount")
    )["total"] or 0

    current_profit = current_income - current_expense

    # ==========================================
    # PROGRESS CALCULATION
    # ==========================================

    for target in targets:

        target.income_progress = (
            (current_income / target.income_target) * 100
            if target.income_target else 0
        )

        target.expense_progress = (
            (current_expense / target.expense_limit) * 100
            if target.expense_limit else 0
        )

        target.profit_progress = (
            (current_profit / target.profit_target) * 100
            if target.profit_target else 0
        )

    # ==========================================
    # PAGINATION
    # ==========================================

    paginator = Paginator(targets, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    # ==========================================
    # CONTEXT
    # ==========================================

    context = {

        "targets": page_obj,

        "page_obj": page_obj,

        "current_income": current_income,

        "current_expense": current_expense,

        "current_profit": current_profit,

        "total_targets": total_targets,

        "total_income_target": total_income_target,

        "total_expense_limit": total_expense_limit,

        "total_profit_target": total_profit_target,

        "active_page": "targets",

        "active_activity": "targets",

    }

    return render(

        request,

        "activity/target_list.html",

        context,

    )




def achievement_list(request):

    achievements = Achievement.objects.all().order_by(
        "-achieved_date",
        "-id"
    )

    paginator = Paginator(
        achievements,
        10
    )

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    context = {

        "achievements": page_obj,

        "page_obj": page_obj,

        "total_achievements": Achievement.objects.count(),

        "monthly_targets": Achievement.objects.filter(
            title__icontains="Target"
        ).count(),

        "revenue_milestones": Achievement.objects.filter(
            title__icontains="Revenue"
        ).count(),

        "business_awards": Achievement.objects.count(),

        "active_page": "achievements",

        "active_activity": "achievements",

    }

    return render(
        request,
        "activity/achievement_list.html",
        context,
    )