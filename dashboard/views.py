from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from django.db.models import Q, Sum
from django.db.models.functions import TruncMonth

import json

from core.services import FinanceService

from income.models import Income
from expenses.models import Expense
from services.models import Project
from training.models import Student

from django.utils import timezone
from datetime import timedelta
from calendar import monthrange
from activity.models import Reminder



today = timezone.localdate()

today_reminders = Reminder.objects.filter(
    reminder_date=today,
    status="Pending"
)

reminder_count = today_reminders.count()
# =====================================================
# DASHBOARD
# =====================================================

@login_required
def dashboard(request):

    # ==================================================
    # MONTHLY TARGET
    # ==================================================

    target = FinanceService.latest_target()

    monthly_target = float(

        target.profit_target if target else 0

    )

    # ==================================================
    # FINANCIAL SUMMARY
    # ==================================================

    total_income = float(

        FinanceService.total_income() or 0

    )

    total_expense = float(

        FinanceService.total_expense() or 0

    )

    net_profit = float(

        FinanceService.net_profit() or 0

    )

    # ==================================================
    # PROGRESS
    # ==================================================

    if monthly_target > 0:

        target_progress = min(

            round(

                (net_profit / monthly_target) * 100

            ),

            100,

        )

        revenue_progress = min(

            round(

                (total_income / monthly_target) * 100

            ),

            100,

        )

    else:

        target_progress = 0

        revenue_progress = 0

    if total_income > 0:

        expense_progress = min(

            round(

                (total_expense / total_income) * 100

            ),

            100,

        )

    else:

        expense_progress = 0

    profit_progress = target_progress

    # ==================================================
    # MONTHLY INCOME CHART
    # ==================================================

    income_chart = (

        Income.objects

        .annotate(

            month=TruncMonth("received_date")

        )

        .values("month")

        .annotate(

            total=Sum("amount")

        )

        .order_by("month")

    )

    expense_chart = (

        Expense.objects

        .annotate(

            month=TruncMonth("expense_date")

        )

        .values("month")

        .annotate(

            total=Sum("amount")

        )

        .order_by("month")

    )

    income_labels = [

        item["month"].strftime("%b")

        for item in income_chart

    ]

    income_values = [

        float(item["total"] or 0)

        for item in income_chart

    ]

    expense_values = [

        float(item["total"] or 0)

        for item in expense_chart

    ]

    # ==================================================
    # INCOME VS EXPENSE FILTER CHART
    # ==================================================

    filter_type = request.GET.get(
        "filter",
        "month"
    )

    today = timezone.localdate()

    week_labels = []

    weekly_income_values = []

    weekly_expense_values = []

    # ==========================================
    # THIS WEEK
    # ==========================================

    if filter_type == "week":

        start = today - timedelta(days=today.weekday())

        for i in range(7):

            current_day = start + timedelta(days=i)

            week_labels.append(
                current_day.strftime("%a")
            )

            income = Income.objects.filter(
                received_date=current_day
            ).aggregate(
                total=Sum("amount")
            )["total"] or 0

            expense = Expense.objects.filter(
                expense_date=current_day
            ).aggregate(
                total=Sum("amount")
            )["total"] or 0

            weekly_income_values.append(float(income))
            weekly_expense_values.append(float(expense))

    # ==========================================
    # THIS MONTH
    # ==========================================

    elif filter_type == "month":

        week_labels = [
            "Week 1",
            "Week 2",
            "Week 3",
            "Week 4",
            "Week 5",
        ]

        weekly_income_values = [0,0,0,0,0]

        weekly_expense_values = [0,0,0,0,0]

        last_day = monthrange(
            today.year,
            today.month
        )[1]

        for day in range(1,last_day+1):

            current = today.replace(day=day)

            week = min((day-1)//7,4)

            income = Income.objects.filter(
                received_date=current
            ).aggregate(
                total=Sum("amount")
            )["total"] or 0

            expense = Expense.objects.filter(
                expense_date=current
            ).aggregate(
                total=Sum("amount")
            )["total"] or 0

            weekly_income_values[week] += float(income)

            weekly_expense_values[week] += float(expense)

    # ==========================================
    # LAST MONTH
    # ==========================================

    elif filter_type == "last_month":

        if today.month == 1:

            year = today.year - 1

            month = 12

        else:

            year = today.year

            month = today.month - 1

        week_labels = [
            "Week 1",
            "Week 2",
            "Week 3",
            "Week 4",
            "Week 5",
        ]

        weekly_income_values = [0,0,0,0,0]

        weekly_expense_values = [0,0,0,0,0]

        last_day = monthrange(
            year,
            month
        )[1]

        for day in range(1,last_day+1):

            current = timezone.datetime(
                year,
                month,
                day
            ).date()

            week = min((day-1)//7,4)

            income = Income.objects.filter(
                received_date=current
            ).aggregate(
                total=Sum("amount")
            )["total"] or 0

            expense = Expense.objects.filter(
                expense_date=current
            ).aggregate(
                total=Sum("amount")
            )["total"] or 0

            weekly_income_values[week] += float(income)

            weekly_expense_values[week] += float(expense)

    # ==========================================
    # THIS YEAR
    # ==========================================

    else:

        week_labels = [

            "Jan","Feb","Mar","Apr","May","Jun",

            "Jul","Aug","Sep","Oct","Nov","Dec"

        ]

        for month in range(1,13):

            income = Income.objects.filter(

                received_date__year=today.year,

                received_date__month=month

            ).aggregate(

                total=Sum("amount")

            )["total"] or 0

            expense = Expense.objects.filter(

                expense_date__year=today.year,

                expense_date__month=month

            ).aggregate(

                total=Sum("amount")

            )["total"] or 0

            weekly_income_values.append(float(income))

            weekly_expense_values.append(float(expense))

    # ==================================================
    # EXPENSE CATEGORY PIE CHART
    # ==================================================

    expense_category = (

        Expense.objects

        .values("category")

        .annotate(

            total=Sum("amount")

        )

        .order_by("category")

    )

    expense_category_labels = [

        item["category"]

        for item in expense_category

    ]

    expense_category_values = [

        float(item["total"] or 0)

        for item in expense_category

    ]
    # ==================================================
    # CONTEXT
    # ==================================================

    context = {
        
        #reminders 
        
        "today_reminders": today_reminders,
        "reminder_count": reminder_count,

        # ----------------------------------------------
        # Notifications
        # ----------------------------------------------

        "unread_notifications": FinanceService.unread_notifications(),

        "recent_notifications": FinanceService.recent_notifications(),

        # ----------------------------------------------
        # Finance Cards
        # ----------------------------------------------

        "total_income": total_income,

        "total_expense": total_expense,

        "net_profit": net_profit,

        "monthly_target": monthly_target,

        "today_income": FinanceService.today_income(),

        "today_expense": FinanceService.today_expense(),

        "monthly_income": FinanceService.monthly_income(),

        "monthly_expense": FinanceService.monthly_expense(),

        # ----------------------------------------------
        # Business
        # ----------------------------------------------

        "total_clients": FinanceService.total_clients(),

        "total_projects": FinanceService.total_projects(),

        "active_projects": FinanceService.active_projects(),

        "completed_projects": FinanceService.completed_projects(),

        "project_revenue": FinanceService.project_revenue(),

        # ----------------------------------------------
        # Training
        # ----------------------------------------------

        "total_students": FinanceService.total_students(),

        "total_courses": FinanceService.total_courses(),

        "active_courses": FinanceService.active_courses(),

        "fees_collected": FinanceService.fees_collected(),

        "pending_fees": FinanceService.pending_fees(),

        "recent_students": FinanceService.recent_students(),

        # ----------------------------------------------
        # Transactions
        # ----------------------------------------------

        "total_transactions": FinanceService.total_transactions(),

        "today_transactions": FinanceService.today_transactions(),

        "recent_transactions": FinanceService.recent_transactions(),

        # ----------------------------------------------
        # Activity Logs (NEW)
        # ----------------------------------------------

        "recent_activities": FinanceService.recent_activity_logs(),

        # ----------------------------------------------
        # Recent Projects
        # ----------------------------------------------

        "recent_projects": FinanceService.recent_projects(),

        # ----------------------------------------------
        # Monthly Charts
        # ----------------------------------------------

        "income_labels": json.dumps(

            income_labels

        ),

        "income_values": json.dumps(

            income_values

        ),

        "expense_values": json.dumps(

            expense_values

        ),

        # ----------------------------------------------
        # Weekly Income vs Expense Chart (NEW)
        # ----------------------------------------------

        "week_labels": json.dumps(
            week_labels
        ),

        "weekly_income_values": json.dumps(
            weekly_income_values
        ),

        "weekly_expense_values": json.dumps(
            weekly_expense_values
        ),

        "selected_filter": filter_type,

        # ----------------------------------------------
        # Expense Category Pie Chart
        # ----------------------------------------------

        "expense_category_labels": json.dumps(

            expense_category_labels

        ),

        "expense_category_values": json.dumps(

            expense_category_values

        ),

        # ----------------------------------------------
        # Progress
        # ----------------------------------------------

        "target_progress": target_progress,

        "revenue_progress": revenue_progress,

        "expense_progress": expense_progress,

        "profit_progress": profit_progress,

    }

    return render(

        request,

        "dashboard/dashboard.html",

        context,

    )
    
# =====================================================
# GLOBAL SEARCH
# =====================================================

def global_search(request):

    query = request.GET.get("q", "").strip()

    results = []

    if not query:

        return JsonResponse(results, safe=False)

    # ==================================================
    # INCOME
    # ==================================================

    incomes = Income.objects.filter(

        Q(income_source__source_name__icontains=query) |

        Q(description__icontains=query)

    )[:5]

    for income in incomes:

        results.append({

            "title": f"Income - ₹{income.amount}",

            "subtitle": income.income_source.source_name,

            "module": "Income",

            "url": "/income/",

        })

    # ==================================================
    # EXPENSE
    # ==================================================

    expenses = Expense.objects.filter(

        Q(expense_name__icontains=query) |

        Q(category__icontains=query)

    )[:5]

    for expense in expenses:

        results.append({

            "title": f"Expense - ₹{expense.amount}",

            "subtitle": expense.expense_name,

            "module": "Expense",

            "url": "/expenses/",

        })

    # ==================================================
    # STUDENTS
    # ==================================================

    students = Student.objects.filter(

        student_name__icontains=query

    )[:5]

    for student in students:

        results.append({

            "title": student.student_name,

            "subtitle": "Student",

            "module": "Training",

            "url": "/training/student/",

        })

    # ==================================================
    # PROJECTS
    # ==================================================

    projects = Project.objects.filter(

        Q(project_name__icontains=query)

    )[:5]

    for project in projects:

        results.append({

            "title": project.project_name,

            "subtitle": "Project",

            "module": "IT Services",

            "url": "/services/",

        })

    return JsonResponse(results, safe=False)