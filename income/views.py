from django.contrib import messages

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator


from transactions.services import TransactionService

from .models import (
    Income,
    CashDenomination,
)
from .forms import (
    IncomeForm,
    CashDenominationFormSet,
)
from django.db.models import Sum
from django.utils import timezone

from activity.services import (
    create_notification,
    log_activity,
)
from django.http import HttpResponse

from openpyxl import Workbook
from openpyxl.styles import Font

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

from reportlab.lib import colors


from activity.models import Achievement, MonthlyTarget
from transactions.models import Transaction

# =====================================================
# INCOME LIST
# =====================================================

def income_list(request):

    incomes = Income.objects.all().order_by("-id")

    search = request.GET.get("search")
    payment_mode = request.GET.get("payment_mode")
    received_date = request.GET.get("received_date")

    if search:
        incomes = incomes.filter(
            Q(income_source__source_name__icontains=search)
            |
            Q(description__icontains=search)
            |
            Q(payment_mode__icontains=search)
        )

    if payment_mode:
        incomes = incomes.filter(
            payment_mode=payment_mode
        )

    if received_date:
        incomes = incomes.filter(
            received_date=received_date
        )

    # ======================================
    # SUMMARY
    # ======================================

    total_income = Income.objects.aggregate(
        total=Sum("amount")
    )["total"] or 0

    today = timezone.now().date()

    today_income = Income.objects.filter(
        received_date=today
    ).aggregate(
        total=Sum("amount")
    )["total"] or 0

    this_month_income = Income.objects.filter(
        received_date__year=today.year,
        received_date__month=today.month
    ).aggregate(
        total=Sum("amount")
    )["total"] or 0

    total_transactions = Income.objects.count()

    # ======================================
    # PAGINATION
    # ======================================

    paginator = Paginator(incomes, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    context = {

        "incomes": page_obj,

        "page_obj": page_obj,

        "search": search,

        "payment_mode": payment_mode,

        "received_date": received_date,

        # Dashboard Cards

        "total_income": total_income,

        "today_income": today_income,

        "this_month_income": this_month_income,

        "total_transactions": total_transactions,

    }

    return render(
        request,
        "income/income.html",
        context
    )


# =====================================================
# ADD INCOME
# =====================================================

def add_income(request):

    form = IncomeForm(

        request.POST or None,

        request.FILES or None,

    )

    if request.method == "POST":
        formset = CashDenominationFormSet(request.POST)
    else:
        formset = CashDenominationFormSet(
            queryset=CashDenomination.objects.none()
        )

    if form.is_valid() and formset.is_valid():

        income = form.save(commit=False)

        income.amount = 0

        income.save()

        total_amount = 0

        for denomination_form in formset:

            if (
                denomination_form.cleaned_data
                and not denomination_form.cleaned_data.get("DELETE", False)
            ):

                cash = denomination_form.save(commit=False)

                cash.income = income

                cash.save()

                total_amount += cash.amount

        income.amount = total_amount

        income.save()

        # ==========================================
        # CREATE TRANSACTION
        # ==========================================

        TransactionService.create_transaction(

            source_module="Income",

            transaction_type="Income",

            reference=income.income_source.source_name,

            amount=income.amount,

            payment_mode=income.payment_mode,

            status="Completed",

            notes=income.description or "",

            user=request.user,

        )

        # ==========================================
        # ACHIEVEMENT CHECK
        # ==========================================

      target = MonthlyTarget.objects.order_by("-id").first()

        if target:

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
            
            print("=" * 50)
            print("TARGET :", target)
            print("CURRENT INCOME :", current_income)
            print("TARGET INCOME :", target.income_target)
            print("CURRENT PROFIT :", current_profit)
            print("TARGET PROFIT :", target.profit_target)
            print("=" * 50)

            # --------------------------------------
            # Income Target Achievement
            # --------------------------------------

            if current_income >= target.income_target:

                print("INSIDE INCOME ACHIEVEMENT")

                achievement, created = Achievement.objects.get_or_create(

                    title="Monthly Income Target Achieved",

                    defaults={

                        "description":
                        "Monthly income target has been successfully achieved."

                    }

                )

                print("CREATED :", created)

            # --------------------------------------
            # Profit Target Achievement
            # --------------------------------------

            if current_profit >= target.profit_target:

                Achievement.objects.get_or_create(

                    title="Profit Goal Achieved",

                    defaults={

                        "description":
                        "Monthly profit goal has been successfully achieved."

                    }

                )

        messages.success(

            request,

            "Income added Successfully."

        )

        return redirect(

            "income_list"

        )

    return render(

        request,

        "income/add.html",

        {

            "form": form,
            "formset": formset,

        }

    )

# =====================================================
# EDIT INCOME
# =====================================================

def edit_income(request, id):

    income = get_object_or_404(

        Income,

        id=id,

    )

    form = IncomeForm(

        request.POST or None,

        request.FILES or None,

        instance=income,

    )
    formset = CashDenominationFormSet(
        request.POST or None,
        instance=income
    )

    if form.is_valid() and formset.is_valid():

        income = form.save(commit=False)

        income.save()

        formset.instance = income

        formset.save()

        total = income.cash_denominations.aggregate(
            total=Sum("amount")
        )["total"] or 0

        income.amount = total

        income.save()

        TransactionService.update_transaction(

            source_module="Income",

            reference=income.income_source.source_name,

            amount=income.amount,

            payment_mode=income.payment_mode,

            status="Completed",

            notes=income.description or "",

            user=request.user,

        )
        messages.success(
            request,
            "Income Updated Successfully."
        )

        return redirect("income_list")

    return render(

        request,
        

        "income/edit.html",

        {

            "form": form,
            "formset": formset,

            "income": income,
            "payment_locked": True,

        }

    )

# =====================================================
# VIEW INCOME
# =====================================================

def view_income(request, id):

    income = get_object_or_404(

        Income,

        id=id,

    )

    log_activity(

        module="Income",

        action="View",

        record_name=income.income_source.source_name,

        description=f"Viewed Income '{income.income_source.source_name}' details.",

        user=request.user,

    )

    return render(

        request,

        "income/view.html",

        {

            "income": income,

        }

    )
# =====================================================
# DELETE INCOME
# =====================================================

def delete_income(request, id):

    income = get_object_or_404(

        Income,

        id=id,

    )

    TransactionService.delete_transaction(

        source_module="Income",

        reference=income.income_source.source_name,

        user=request.user,

    )

    income.delete()
    messages.success(
        request,
        "Income Deleted Successfully."
    )

    return redirect("income_list")



def get_filtered_income(request):

    incomes = Income.objects.all().order_by("-id")

    search = request.GET.get("search")
    payment_mode = request.GET.get("payment_mode")
    received_date = request.GET.get("received_date")

    if search:

        incomes = incomes.filter(

            Q(income_source__source_name__icontains=search)

            |

            Q(description__icontains=search)

            |

            Q(payment_mode__icontains=search)

        )

    if payment_mode:

        incomes = incomes.filter(

            payment_mode=payment_mode

        )

    if received_date:

        incomes = incomes.filter(

            received_date=received_date

        )

    return incomes

# =====================================================
# EXPORT INCOME EXCEL
# =====================================================

def export_income_excel(request):

    workbook = Workbook()

    sheet = workbook.active

    sheet.title = "Income Report"

    headers = [

        "S.No",

        "Income Source",

        "Amount (₹)",

        "Payment Mode",

        "Received Date",

        "Description",

    ]

    sheet.append(headers)

    # Header Style
    for cell in sheet[1]:

        cell.font = Font(bold=True)

    incomes = get_filtered_income(request)

    for index, income in enumerate(incomes, start=1):

        sheet.append([

            index,

            income.income_source.source_name,

            float(income.amount),

            income.payment_mode,

            income.received_date.strftime("%d-%m-%Y"),

            income.description if income.description else "-",

        ])

    # Auto Width
    for column_cells in sheet.columns:

        length = max(len(str(cell.value)) if cell.value else 0 for cell in column_cells)

        sheet.column_dimensions[column_cells[0].column_letter].width = length + 5

    response = HttpResponse(

        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    )

    response["Content-Disposition"] = 'attachment; filename="Income_Report.xlsx"'

    workbook.save(response)

    return response

def export_income_pdf(request):

    response = HttpResponse(content_type="application/pdf")

    response["Content-Disposition"] = 'attachment; filename="Income_Report.pdf"'

    document = SimpleDocTemplate(response)

    data = [[
        "Source",
        "Amount",
        "Payment",
        "Date",
    ]]

    incomes = get_filtered_income(request)

    for income in incomes:

        data.append([

            income.income_source,

            f"₹ {income.amount}",

            income.payment_mode,

            str(income.received_date),

        ])

    table = Table(data)

    table.setStyle(

        TableStyle([

            ("BACKGROUND",(0,0),(-1,0),colors.green),

            ("TEXTCOLOR",(0,0),(-1,0),colors.white),

            ("GRID",(0,0),(-1,-1),1,colors.grey),

            ("BACKGROUND",(0,1),(-1,-1),colors.beige),

            ("ALIGN",(0,0),(-1,-1),"CENTER"),

            ("BOTTOMPADDING",(0,0),(-1,0),10),

        ])

    )

    document.build([table])

    return response

