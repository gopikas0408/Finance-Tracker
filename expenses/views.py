from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages

from .models import Expense
from .forms import (
    ExpenseForm,
    ExpenseCashDenominationFormSet,
    ExpenseCashDenominationEditFormSet,
)
import openpyxl

from transactions.services import TransactionService

from django.http import HttpResponse
from django.db.models import Q, Sum
from django.utils import timezone

from reportlab.pdfgen import canvas

from activity.services import (
    create_notification,
    log_activity,
)
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
)

# =====================================================
# EXPENSE LIST
# =====================================================

def expense_list(request):

    expenses = Expense.objects.all().order_by("-id")

    search = request.GET.get("search")
    payment_mode = request.GET.get("payment_mode")
    expense_date = request.GET.get("expense_date")

    if search:
        expenses = expenses.filter(
            Q(expense_name__icontains=search) |
            Q(description__icontains=search) |
            Q(payment_mode__icontains=search)
        )

    if payment_mode:
        expenses = expenses.filter(
            payment_mode=payment_mode
        )

    if expense_date:
        expenses = expenses.filter(
            expense_date=expense_date
        )

    # -----------------------------
    # Dashboard Cards
    # -----------------------------

    today = timezone.localdate()

    total_expense = expenses.aggregate(
        total=Sum("amount")
    )["total"] or 0

    this_month_expense = expenses.filter(
        expense_date__year=today.year,
        expense_date__month=today.month
    ).aggregate(
        total=Sum("amount")
    )["total"] or 0

    today_expense = expenses.filter(
        expense_date=today
    ).aggregate(
        total=Sum("amount")
    )["total"] or 0

    total_entries = expenses.count()

    paginator = Paginator(expenses, 5)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    context = {

        "expenses": page_obj,
        "page_obj": page_obj,

        "search": search,
        "payment_mode": payment_mode,
        "expense_date": expense_date,

        # Dashboard Cards
        "total_expense": total_expense,
        "this_month_expense": this_month_expense,
        "today_expense": today_expense,
        "total_entries": total_entries,

    }

    return render(
        request,
        "expenses/expenses.html",
        context,
    )
# =====================================================
# ADD EXPENSE
# =====================================================

def add_expense(request):

    form = ExpenseForm(

        request.POST or None,

        request.FILES or None,

    )
    
    if request.method == "POST":
        formset = ExpenseCashDenominationFormSet(request.POST)
    else:
        formset = ExpenseCashDenominationFormSet()

    if form.is_valid() and formset.is_valid():
        
        expense = form.save(commit=False)

        expense.save()

        formset.instance = expense

        formset.save()

        total = expense.cash_denominations.aggregate(
            total=Sum("amount")
        )["total"] or 0

        expense.amount = total

        expense.save()

        TransactionService.create_transaction(

            source_module="Expense",

            transaction_type="Expense",

            reference=expense.expense_name,

            amount=expense.amount,

            payment_mode=expense.payment_mode,

            status="Completed",

            notes=expense.description or "",

            user=request.user,

        )

        messages.success(

            request,

            "Expense added successfully."

        )

        return redirect("expenses:expense_list")

    return render(

        request,

        "expenses/add.html",

        {

            "form": form,
            "formset": formset,

        },

    )

# =====================================================
# EDIT EXPENSE
# =====================================================

def edit_expense(request, id):

    expense = get_object_or_404(

        Expense,

        id=id,

    )

    form = ExpenseForm(

        request.POST or None,

        request.FILES or None,

        instance=expense,

    )
    formset = ExpenseCashDenominationEditFormSet(
        request.POST or None,
        instance=expense
    )

    if form.is_valid() and formset.is_valid():

        expense = form.save(commit=False)

        expense.save()

        formset.instance = expense

        formset.save()

        total = expense.cash_denominations.aggregate(
            total=Sum("amount")
        )["total"] or 0

        expense.amount = total

        expense.save()

        TransactionService.update_transaction(

            source_module="Expense",

            reference=expense.expense_name,

            amount=expense.amount,

            payment_mode=expense.payment_mode,

            status="Completed",

            notes=expense.description or "",

            user=request.user,

        )

        messages.success(

            request,

            "Expense updated successfully."

        )

        return redirect("expenses:expense_list")

    return render(

        request,

        "expenses/edit.html",

        {

            "form": form,
            "formset": formset,

            "expense": expense,
            "payment_locked": True,

        },

    )


# =====================================================
# VIEW EXPENSE
# =====================================================

def view_expense(request, id):

    expense = get_object_or_404(

        Expense,

        id=id,

    )

    log_activity(

        module="Expense",

        action="View",

        record_name=expense.expense_name,

        description=f"Viewed Expense '{expense.expense_name}' details.",

        user=request.user,

    )

    return render(

        request,

        "expenses/view.html",

        {

            "expense": expense,

        },

    )


# =====================================================
# DELETE EXPENSE
# =====================================================

def delete_expense(request, id):

    expense = get_object_or_404(

        Expense,

        id=id,

    )

    TransactionService.delete_transaction(

        source_module="Expense",

        reference=expense.expense_name,

        user=request.user,

    )

    expense.delete()

    messages.success(

        request,

        "Expense deleted successfully."

    )

    return redirect("expenses:expense_list")

# =====================================================
# FILTERED EXPENSE QUERY
# =====================================================

def get_filtered_expenses(request):

    expenses = Expense.objects.all().order_by("-id")

    search = request.GET.get("search")

    payment_mode = request.GET.get("payment_mode")

    expense_date = request.GET.get("expense_date")

    if search:

        expenses = expenses.filter(

            Q(expense_name__icontains=search)

            |

            Q(description__icontains=search)

            |

            Q(payment_mode__icontains=search)

        )

    if payment_mode:

        expenses = expenses.filter(

            payment_mode=payment_mode

        )

    if expense_date:

        expenses = expenses.filter(

            expense_date=expense_date

        )

    return expenses

def export_expense_excel(request):

    workbook = openpyxl.Workbook()

    sheet = workbook.active

    sheet.title = "Expenses"

    sheet.append([
        "Expense",
        "Category",
        "Amount",
        "Payment Mode",
        "Expense Date",
    ])

    expenses = get_filtered_expenses(request)

    for expense in expenses:

        sheet.append([
            expense.expense_name,
            expense.category,
            float(expense.amount),
            expense.payment_mode,
            str(expense.expense_date),
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response["Content-Disposition"] = 'attachment; filename="Expenses.xlsx"'

    workbook.save(response)

    return response





# =====================================================
# EXPORT EXPENSE PDF
# =====================================================

def export_expense_pdf(request):

    response = HttpResponse(
        content_type="application/pdf"
    )

    response["Content-Disposition"] = (
        'attachment; filename="Expense_Report.pdf"'
    )

    document = SimpleDocTemplate(response)

    styles = getSampleStyleSheet()

    title_style = styles["Heading1"]

    title_style.alignment = TA_CENTER

    elements = []

    elements.append(
        Paragraph(
            "Expense Report",
            title_style,
        )
    )

    elements.append(
        Spacer(1, 20)
    )

    data = [[

        "S.No",

        "Expense Name",

        "Category",

        "Amount (₹)",

        "Payment",

        "Date",

    ]]

    expenses = get_filtered_expenses(request)

    for index, expense in enumerate(expenses, start=1):

        data.append([

            index,

            expense.expense_name,

            expense.category,

            f"₹ {expense.amount}",

            expense.payment_mode,

            expense.expense_date.strftime("%d-%m-%Y"),

        ])

    table = Table(

        data,

        colWidths=[40, 140, 90, 80, 80, 80]

    )

    table.setStyle(

        TableStyle([

            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#0F4C81")),

            ("TEXTCOLOR", (0,0), (-1,0), colors.white),

            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),

            ("FONTSIZE", (0,0), (-1,0), 11),

            ("BOTTOMPADDING", (0,0), (-1,0), 10),

            ("BACKGROUND", (0,1), (-1,-1), colors.whitesmoke),

            ("GRID", (0,0), (-1,-1), 0.5, colors.grey),

            ("ALIGN", (0,0), (-1,-1), "CENTER"),

            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),

            ("FONTNAME", (0,1), (-1,-1), "Helvetica"),

            ("FONTSIZE", (0,1), (-1,-1), 10),

            ("ROWBACKGROUNDS",
             (0,1),
             (-1,-1),
             [colors.white, colors.HexColor("#F7F9FC")]),

        ])

    )

    elements.append(table)

    document.build(elements)

    return response