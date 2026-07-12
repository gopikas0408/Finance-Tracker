from urllib import request

from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Sum
from django.core.paginator import Paginator
from django.http import HttpResponse

from openpyxl import Workbook
from openpyxl.styles import Font

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
)

from reportlab.lib import colors

from .models import Transaction

from activity.services import (
    log_activity,
)


# =====================================================
# TRANSACTION LIST
# =====================================================

def transaction_list(request):

    transactions = Transaction.objects.all().order_by("-created_at")

    search = request.GET.get("search", "").strip()

    if search == "None":
        search = ""
    transaction_type = request.GET.get("transaction_type")
    status = request.GET.get("status")
    source_module = request.GET.get("source_module")
    payment_mode = request.GET.get("payment_mode")
    
    print("=" * 50)
    print("GET DATA :", request.GET)
    print("Search :", search)
    print("Transaction Type :", transaction_type)
    print("Status :", status)
    print("=" * 50)

    # ==========================================
    # SEARCH
    # ==========================================

    if search and search.lower() != "none":

        transactions = transactions.filter(

            Q(transaction_id__icontains=search) |

            Q(reference__icontains=search)

        )

    # ==========================================
    # FILTERS
    # ==========================================

    if transaction_type:

        transactions = transactions.filter(

            transaction_type=transaction_type

        )

    if status:

        transactions = transactions.filter(

            status=status

        )

    if source_module:

        transactions = transactions.filter(

            source_module=source_module

        )

    if payment_mode:

        transactions = transactions.filter(

            payment_mode=payment_mode

        )

    # ==========================================
    # SUMMARY CARDS
    # ==========================================

    total_transactions = Transaction.objects.count()

    total_income = Transaction.objects.filter(

        transaction_type="Income"

    ).aggregate(

        total=Sum("amount")

    )["total"] or 0

    total_expense = Transaction.objects.filter(

        transaction_type="Expense"

    ).aggregate(

        total=Sum("amount")

    )["total"] or 0

    total_amount = Transaction.objects.aggregate(

        total=Sum("amount")

    )["total"] or 0

    completed_transactions = Transaction.objects.filter(

        status="Completed"

    ).count()

    pending_transactions = Transaction.objects.filter(

        status="Pending"

    ).count()

    failed_transactions = Transaction.objects.filter(

        status="Failed"

    ).count()

    # ==========================================
    # PAGINATION
    # ==========================================

    paginator = Paginator(

        transactions,

        10,

    )

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    context = {

        "transactions": page_obj,

        "page_obj": page_obj,

        "search": search,

        "transaction_type": transaction_type,

        "status": status,

        "source_module": source_module,

        "payment_mode": payment_mode,

        # Summary Cards
        "total_transactions": total_transactions,

        "total_income": total_income,

        "total_expense": total_expense,

        "total_amount": total_amount,

        "completed_transactions": completed_transactions,

        "pending_transactions": pending_transactions,

        "failed_transactions": failed_transactions,

        "active_page": "transactions",

    }

    return render(

        request,

        "transactions/transactions.html",

        context,

    )
    
# =====================================================
# VIEW TRANSACTION
# =====================================================

def view_transaction(request, id):

    transaction = get_object_or_404(

        Transaction,

        id=id,

    )

    # ==========================================
    # ACTIVITY LOG
    # ==========================================

    log_activity(

        module="Transactions",

        action="View",

        record_name=transaction.transaction_id,

        description=(

            f"Viewed {transaction.transaction_type} "

            f"Transaction ({transaction.transaction_id}) "

            f"for '{transaction.reference}'."

        ),

        user=request.user,

    )

    context = {

        "transaction": transaction,

        "active_page": "transactions",

    }

    return render(

        request,

        "transactions/view.html",

        context,

    )
# =====================================================
# EXPORT TRANSACTION EXCEL
# =====================================================

def export_transaction_excel(request):

    workbook = Workbook()

    sheet = workbook.active

    sheet.title = "Transaction Report"

    headers = [

        "Transaction ID",

        "Source Module",

        "Transaction Type",

        "Reference",

        "Amount (₹)",

        "Payment Mode",

        "Transaction Date",

        "Status",

        "Notes",

    ]

    sheet.append(headers)

    # Header Style

    for cell in sheet[1]:

        cell.font = Font(bold=True)

    transactions = Transaction.objects.all().order_by("-created_at")

    for transaction in transactions:

        sheet.append([

            transaction.transaction_id,

            transaction.source_module,

            transaction.transaction_type,

            transaction.reference,

            float(transaction.amount),

            transaction.payment_mode,

            transaction.transaction_date.strftime("%d-%m-%Y"),

            transaction.status,

            transaction.notes if transaction.notes else "-",

        ])

    # Auto Width

    for column_cells in sheet.columns:

        length = max(

            len(str(cell.value))

            if cell.value else 0

            for cell in column_cells

        )

        sheet.column_dimensions[

            column_cells[0].column_letter

        ].width = length + 5

    response = HttpResponse(

        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    )

    response["Content-Disposition"] = 'attachment; filename="Transaction_Report.xlsx"'

    workbook.save(response)

    return response
# =====================================================
# EXPORT TRANSACTION PDF
# =====================================================

def export_transaction_pdf(request):

    response = HttpResponse(

        content_type="application/pdf"

    )

    response["Content-Disposition"] = 'attachment; filename="Transaction_Report.pdf"'

    document = SimpleDocTemplate(response)

    data = [[

        "ID",

        "Module",

        "Type",

        "Reference",

        "Amount",

        "Payment",

        "Status",

        "Date",

    ]]

    transactions = Transaction.objects.all().order_by("-created_at")

    for transaction in transactions:

        data.append([

            transaction.transaction_id,

            transaction.source_module,

            transaction.transaction_type,

            transaction.reference,

            f"₹ {transaction.amount}",

            transaction.payment_mode,

            transaction.status,

            transaction.transaction_date.strftime("%d-%m-%Y"),

        ])

    table = Table(data)

    table.setStyle(

        TableStyle([

            ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),

            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

            ("GRID", (0, 0), (-1, -1), 1, colors.grey),

            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),

            ("ALIGN", (0, 0), (-1, -1), "CENTER"),

            ("BOTTOMPADDING", (0, 0), (-1, 0), 10),

            ("FONTSIZE", (0, 0), (-1, -1), 9),

        ])

    )

    document.build([table])

    return response