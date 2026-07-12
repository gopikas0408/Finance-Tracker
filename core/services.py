from datetime import date, timedelta

from django.db.models import (
    Sum,
    Count,
)

from django.db.models.functions import (
    TruncWeek,
    TruncMonth,
)

from income.models import Income
from expenses.models import Expense

from dashboard.models import MonthlyTarget

from transactions.models import Transaction

from training.models import (
    Student,
    StudentPayment,
    Course,
)

from services.models import (
    Client,
    Project,
    ProjectPayment,
    ProjectExpense,
    EmployeeSalary,
)

from activity.models import (
    Notification,
    ActivityLog,
)

from activity.models import Notification


# ==========================================================
# FINANCE SERVICE
# ==========================================================

class FinanceService:

    """
    Central Dashboard Service

    This service is responsible for

    ✔ Dashboard Cards
    ✔ Charts
    ✔ Recent Transactions
    ✔ Recent Activities
    ✔ Notifications
    ✔ Income
    ✔ Expenses
    ✔ IT Services
    ✔ IT Training
    ✔ Analytics

    """
    # ==========================================================
    # TOTAL INCOME
    # ==========================================================

    @staticmethod
    def total_income():

        income = Income.objects.aggregate(

            total=Sum("amount")

        )["total"] or 0

        training_income = StudentPayment.objects.aggregate(

            total=Sum("amount")

        )["total"] or 0

        service_income = ProjectPayment.objects.aggregate(

            total=Sum("amount")

        )["total"] or 0

        return (

            income

            +

            training_income

            +

            service_income

        )


    # ==========================================================
    # TOTAL EXPENSE
    # ==========================================================

    @staticmethod
    def total_expense():

        office_expense = Expense.objects.aggregate(

            total=Sum("amount")

        )["total"] or 0

        project_expense = ProjectExpense.objects.aggregate(

            total=Sum("amount")

        )["total"] or 0

        employee_salary = EmployeeSalary.objects.aggregate(

            total=Sum("net_salary")

        )["total"] or 0

        return (

            office_expense

            +

            project_expense

            +

            employee_salary

        )
        
        
    @staticmethod
    def unread_notifications():

        return Notification.objects.filter(
            is_read=False
        ).count()
        
    @staticmethod
    def recent_notifications():
        return Notification.objects.order_by(
            "-created_at"
        )[:5]


    # ==========================================================
    # NET PROFIT
    # ==========================================================

    @staticmethod
    def net_profit():

        return (

            FinanceService.total_income()

            -

            FinanceService.total_expense()

        )


    # ==========================================================
    # LATEST TARGET
    # ==========================================================

    @staticmethod
    def latest_target():

        return MonthlyTarget.objects.order_by(

            "-created_at"

        ).first()
        
        # ==========================================================
    # CLIENTS
    # ==========================================================

    @staticmethod
    def total_clients():

        return Client.objects.count()


    # ==========================================================
    # PROJECTS
    # ==========================================================

    @staticmethod
    def total_projects():

        return Project.objects.count()


    # ==========================================================
    # ACTIVE PROJECTS
    # ==========================================================

    @staticmethod
    def active_projects():

        return Project.objects.filter(

            status="Active"

        ).count()


    # ==========================================================
    # COMPLETED PROJECTS
    # ==========================================================

    @staticmethod
    def completed_projects():

        return Project.objects.filter(

            status="Completed"

        ).count()


    # ==========================================================
    # RUNNING PROJECTS
    # ==========================================================

    @staticmethod
    def running_projects():

        return Project.objects.filter(

            status="Running"

        ).count()


    # ==========================================================
    # PROJECT REVENUE
    # ==========================================================

    @staticmethod
    def project_revenue():

        return ProjectPayment.objects.aggregate(

            total=Sum("amount")

        )["total"] or 0


    # ==========================================================
    # PROJECT EXPENSE
    # ==========================================================

    @staticmethod
    def project_expense():

        return ProjectExpense.objects.aggregate(

            total=Sum("amount")

        )["total"] or 0


    # ==========================================================
    # EMPLOYEE SALARY
    # ==========================================================

    @staticmethod
    def employee_salary():

        return EmployeeSalary.objects.aggregate(

            total=Sum("net_salary")

        )["total"] or 0


    # ==========================================================
    # SERVICE PROFIT
    # ==========================================================

    @staticmethod
    def service_profit():

        revenue = FinanceService.project_revenue()

        expense = (

            FinanceService.project_expense()

            +

            FinanceService.employee_salary()

        )

        return revenue - expense


    # ==========================================================
    # RECENT PROJECTS
    # ==========================================================

    @staticmethod
    def recent_projects():

        return Project.objects.select_related(

            "client"

        ).order_by(

            "-created_at"

        )[:5]
        
        
    # ==========================================================
    # TOTAL STUDENTS
    # ==========================================================

    @staticmethod
    def total_students():

        return Student.objects.count()


    # ==========================================================
    # TOTAL COURSES
    # ==========================================================

    @staticmethod
    def total_courses():

        return Course.objects.count()


    # ==========================================================
    # ACTIVE STUDENTS
    # ==========================================================

    @staticmethod
    def active_students():

        return Student.objects.filter(

            status="Active"

        ).count()


    # ==========================================================
    # ACTIVE COURSES
    # ==========================================================

    @staticmethod
    def active_courses():

        return Course.objects.filter(

            status="Active"

        ).count()


    # ==========================================================
    # FEES COLLECTED
    # ==========================================================

    @staticmethod
    def fees_collected():

        return StudentPayment.objects.aggregate(

            total=Sum("amount")

        )["total"] or 0


    # ==========================================================
    # PENDING FEES
    # ==========================================================




    @staticmethod
    def pending_fees():

        total_pending = 0

        students = Student.objects.all()

        for student in students:

            total_paid = StudentPayment.objects.filter(
                student=student
            ).aggregate(
                total=Sum("amount")
            )["total"] or 0

            balance = student.course_fee - total_paid

            if balance > 0:
                total_pending += balance

        return total_pending


    # ==========================================================
    # TODAY'S FEES
    # ==========================================================

    @staticmethod
    def today_fees():

        return StudentPayment.objects.filter(

            payment_date=date.today()

        ).aggregate(

            total=Sum("amount")

        )["total"] or 0


    # ==========================================================
    # MONTHLY FEES
    # ==========================================================

    @staticmethod
    def monthly_fees():

        return StudentPayment.objects.filter(

            payment_date__month=date.today().month,

            payment_date__year=date.today().year

        ).aggregate(

            total=Sum("amount")

        )["total"] or 0


    # ==========================================================
    # RECENT STUDENTS
    # ==========================================================

    @staticmethod
    def recent_students():

        return Student.objects.select_related(

            "course"

        ).order_by(

            "-created_at"

        )[:5]
        
        # ==========================================================
    # TOTAL TRANSACTIONS
    # ==========================================================

    @staticmethod
    def total_transactions():

        return Transaction.objects.count()


    # ==========================================================
    # TODAY'S TRANSACTIONS
    # ==========================================================

    @staticmethod
    def today_transactions():

        return Transaction.objects.filter(

            transaction_date=date.today()

        ).count()


    # ==========================================================
    # RECENT TRANSACTIONS
    # ==========================================================

    @staticmethod
    def recent_transactions():

        return Transaction.objects.select_related(

            "created_by"

        ).order_by(

            "-created_at"

        )[:4]


    # ==========================================================
    # TRANSACTION SUMMARY
    # ==========================================================

    @staticmethod
    def income_transactions():

        return Transaction.objects.filter(

            transaction_type="Income"

        ).count()


    @staticmethod
    def expense_transactions():

        return Transaction.objects.filter(

            transaction_type="Expense"

        ).count()


    @staticmethod
    def completed_transactions():

        return Transaction.objects.filter(

            status="Completed"

        ).count()


    @staticmethod
    def pending_transactions():

        return Transaction.objects.filter(

            status="Pending"

        ).count()


    @staticmethod
    def failed_transactions():

        return Transaction.objects.filter(

            status="Failed"

        ).count()


    # ==========================================================
    # RECENT ACTIVITY LOGS
    # ==========================================================

    @staticmethod
    def recent_activity_logs():

        return ActivityLog.objects.select_related(

            "user"

        ).order_by(

            "-created_at"

        )[:3]


    # ==========================================================
    # RECENT NOTIFICATIONS
    # ==========================================================

    @staticmethod
    def recent_notifications():

        return Notification.objects.order_by(

            "-created_at"

        )[:5]


    # ==========================================================
    # UNREAD NOTIFICATIONS
    # ==========================================================

    @staticmethod
    def unread_notifications():

        return Notification.objects.filter(

            is_read=False

        ).count()


    # ==========================================================
    # TOTAL NOTIFICATIONS
    # ==========================================================

    @staticmethod
    def total_notifications():

        return Notification.objects.count()
    
        # ==========================================================
    # TODAY'S INCOME
    # ==========================================================

    @staticmethod
    def today_income():

        return Income.objects.filter(

            received_date=date.today()

        ).aggregate(

            total=Sum("amount")

        )["total"] or 0


    # ==========================================================
    # TODAY'S EXPENSE
    # ==========================================================

    @staticmethod
    def today_expense():

        return Expense.objects.filter(

            expense_date=date.today()

        ).aggregate(

            total=Sum("amount")

        )["total"] or 0


    # ==========================================================
    # MONTHLY INCOME
    # ==========================================================

    @staticmethod
    def monthly_income():

        today = date.today()

        return Income.objects.filter(

            received_date__year=today.year,

            received_date__month=today.month,

        ).aggregate(

            total=Sum("amount")

        )["total"] or 0


    # ==========================================================
    # MONTHLY EXPENSE
    # ==========================================================

    @staticmethod
    def monthly_expense():

        today = date.today()

        return Expense.objects.filter(

            expense_date__year=today.year,

            expense_date__month=today.month,

        ).aggregate(

            total=Sum("amount")

        )["total"] or 0


    # ==========================================================
    # WEEKLY INCOME CHART
    # ==========================================================

    @staticmethod
    def weekly_income_chart():

        return (

            Income.objects

            .annotate(

                week=TruncWeek("received_date")

            )

            .values("week")

            .annotate(

                total=Sum("amount")

            )

            .order_by("week")

        )


    # ==========================================================
    # WEEKLY EXPENSE CHART
    # ==========================================================

    @staticmethod
    def weekly_expense_chart():

        return (

            Expense.objects

            .annotate(

                week=TruncWeek("expense_date")

            )

            .values("week")

            .annotate(

                total=Sum("amount")

            )

            .order_by("week")

        )


    # ==========================================================
    # MONTHLY INCOME CHART
    # ==========================================================

    @staticmethod
    def monthly_income_chart():

        return (

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


    # ==========================================================
    # MONTHLY EXPENSE CHART
    # ==========================================================

    @staticmethod
    def monthly_expense_chart():

        return (

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


    # ==========================================================
    # EXPENSE CATEGORY CHART
    # ==========================================================

    @staticmethod
    def expense_category_chart():

        return (

            Expense.objects

            .values(

                "category"

            )

            .annotate(

                total=Sum("amount")

            )

            .order_by(

                "category"

            )

        )


    # ==========================================================
    # DASHBOARD SUMMARY
    # ==========================================================

    @staticmethod
    def dashboard_summary():

        return {

            "income": FinanceService.total_income(),

            "expense": FinanceService.total_expense(),

            "profit": FinanceService.net_profit(),

            "clients": FinanceService.total_clients(),

            "projects": FinanceService.total_projects(),

            "students": FinanceService.total_students(),

            "transactions": FinanceService.total_transactions(),

        }