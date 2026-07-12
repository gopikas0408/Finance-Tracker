from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Sum
from django.core.paginator import Paginator

from .models import Client, Project, ProjectPayment, ProjectExpense, EmployeeSalary
from .forms import ClientForm, ProjectForm, ProjectPaymentForm, ProjectExpenseForm, EmployeeSalaryForm
from datetime import date
from django.http import HttpResponse
from openpyxl import Workbook
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from reportlab.lib.units import inch
from activity.services import (
    create_notification,
    log_activity,
)
from transactions.services import TransactionService


# ======================================================
# CLIENT LIST
# ======================================================

def client_list(request):

    clients = Client.objects.all().order_by("-id")

    search = request.GET.get("search", "")

    if search:
        clients = clients.filter(
            Q(company_name__icontains=search) |
            Q(contact_person__icontains=search) |
            Q(email__icontains=search) |
            Q(phone__icontains=search)
        )

    paginator = Paginator(clients, 5)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    context = {

        "clients": page_obj,

        "page_obj": page_obj,

        "search": search,

        "active_page": "clients",

        # ==========================
        # REAL TIME SUMMARY
        # ==========================

        "total_clients": Client.objects.count(),

        "active_clients": Client.objects.filter(
            status="Active"
        ).count(),

        "running_projects": Project.objects.filter(
            status="Running"
        ).count(),

        "client_revenue": ProjectPayment.objects.aggregate(
            total=Sum("amount")
        )["total"] or 0,

    }

    return render(
        request,
        "services/client_list.html",
        context
    )


def add_client(request):

    form = ClientForm(request.POST or None)

    if form.is_valid():

        client = form.save()

        create_notification(

            title="Client Added",

            message=f"{client.company_name} added successfully.",

            module="Services",

            action="Add",

            priority="Medium",

            user=request.user,

        )

        log_activity(

            module="Services",

            action="Add",

            record_name=client.company_name,

            description="New client registered.",

            user=request.user,

        )

        messages.success(

            request,

            "Client Added Successfully."

        )

        return redirect("client_list")

    return render(

        request,

        "services/add_client.html",

        {

            "form": form

        }

    )


def edit_client(request, id):

    client = get_object_or_404(

        Client,

        id=id

    )

    form = ClientForm(

        request.POST or None,

        instance=client

    )

    if form.is_valid():

        client = form.save()

        create_notification(

            title="Client Updated",

            message=f"{client.company_name} updated successfully.",

            module="Services",

            action="Edit",

            priority="Low",

            user=request.user,

        )

        log_activity(

            module="Services",

            action="Edit",

            record_name=client.company_name,

            description="Client details updated.",

            user=request.user,

        )

        messages.success(

            request,

            "Client Updated Successfully."

        )

        return redirect("client_list")

    return render(

        request,

        "services/edit_client.html",

        {

            "form": form,

            "client": client

        }

    )


def view_client(request, id):

    client = get_object_or_404(

        Client,

        id=id

    )

    log_activity(

        module="Services",

        action="View",

        record_name=client.company_name,

        description="Viewed client details.",

        user=request.user,

    )

    return render(

        request,

        "services/view_client.html",

        {

            "client": client

        }

    )


def delete_client(request, id):

    client = get_object_or_404(

        Client,

        id=id

    )

    create_notification(

        title="Client Deleted",

        message=f"{client.company_name} deleted.",

        module="Services",

        action="Delete",

        priority="High",

        user=request.user,

    )

    log_activity(

        module="Services",

        action="Delete",

        record_name=client.company_name,

        description="Client deleted from the system.",

        user=request.user,

    )

    client.delete()

    messages.success(

        request,

        "Client Deleted Successfully."

    )

    return redirect("client_list")


# ======================================================
# PROJECT LIST
# ======================================================

def project_list(request):

    projects = Project.objects.select_related(
        "client"
    ).all().order_by("-id")

    search = request.GET.get("search", "")

    if search:

        projects = projects.filter(

            Q(project_name__icontains=search) |

            Q(client__company_name__icontains=search)

        )

    paginator = Paginator(projects, 5)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    context = {

        "projects": page_obj,

        "page_obj": page_obj,

        "search": search,

        "active_page": "projects",

        # ===================================
        # REAL TIME SUMMARY CARDS
        # ===================================

        "total_projects": Project.objects.count(),

        "running_projects": Project.objects.filter(
            status="Running"
        ).count(),

        "completed_projects": Project.objects.filter(
            status="Completed"
        ).count(),

        "project_revenue": ProjectPayment.objects.aggregate(
            total=Sum("amount")
        )["total"] or 0,

    }

    return render(

        request,

        "services/project_list.html",

        context

    )


def add_project(request):

    form = ProjectForm(request.POST or None)

    if form.is_valid():

        project = form.save()

        create_notification(

            title="Project Added",

            message=f"{project.project_name} project created successfully.",

            module="Services",

            action="Add",

            priority="Medium",

            user=request.user,

        )

        log_activity(

            module="Services",

            action="Add",

            record_name=project.project_name,

            description=f"Project created for {project.client.company_name}.",

            user=request.user,

        )

        messages.success(

            request,

            "Project Added Successfully."

        )

        return redirect("project_list")

    return render(

        request,

        "services/add_project.html",

        {

            "form": form

        }

    )


def edit_project(request, id):

    project = get_object_or_404(

        Project,

        id=id

    )

    form = ProjectForm(

        request.POST or None,

        instance=project

    )

    if form.is_valid():

        project = form.save()

        create_notification(

            title="Project Updated",

            message=f"{project.project_name} updated successfully.",

            module="Services",

            action="Edit",

            priority="Low",

            user=request.user,

        )

        log_activity(

            module="Services",

            action="Edit",

            record_name=project.project_name,

            description="Project information updated.",

            user=request.user,

        )

        messages.success(

            request,

            "Project Updated Successfully."

        )

        return redirect("project_list")

    return render(

        request,

        "services/edit_project.html",

        {

            "form": form,

            "project": project

        }

    )


def view_project(request, id):

    project = get_object_or_404(

        Project,

        id=id

    )

    log_activity(

        module="Services",

        action="View",

        record_name=project.project_name,

        description="Viewed project details.",

        user=request.user,

    )

    return render(

        request,

        "services/view_project.html",

        {

            "project": project

        }

    )


def delete_project(request, id):

    project = get_object_or_404(

        Project,

        id=id

    )

    create_notification(

        title="Project Deleted",

        message=f"{project.project_name} deleted.",

        module="Services",

        action="Delete",

        priority="High",

        user=request.user,

    )

    log_activity(

        module="Services",

        action="Delete",

        record_name=project.project_name,

        description="Project deleted from the system.",

        user=request.user,

    )

    project.delete()

    messages.success(

        request,

        "Project Deleted Successfully."

    )

    return redirect("project_list")

# ======================================================
# PROJECT PAYMENTS
# ======================================================

def payment_list(request):

    payments = ProjectPayment.objects.select_related(
        "project"
    ).all().order_by("-id")

    search = request.GET.get("search", "")

    if search:

        payments = payments.filter(

            Q(project__project_name__icontains=search) |

            Q(project__client__company_name__icontains=search)

        )

    paginator = Paginator(payments, 5)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    context = {

        "payments": page_obj,

        "page_obj": page_obj,

        "search": search,

        "active_page": "payments",

        # ===================================
        # REAL TIME SUMMARY CARDS
        # ===================================

        "total_payments": ProjectPayment.objects.count(),

        "total_amount": ProjectPayment.objects.aggregate(
            total=Sum("amount")
        )["total"] or 0,

        "today_payments": ProjectPayment.objects.filter(
            payment_date=date.today()
        ).aggregate(
            total=Sum("amount")
        )["total"] or 0,

        "this_month_payments": ProjectPayment.objects.filter(
            payment_date__year=date.today().year,
            payment_date__month=date.today().month
        ).aggregate(
            total=Sum("amount")
        )["total"] or 0,

    }

    return render(

        request,

        "services/payment_list.html",

        context

    )

# ======================================================
# ADD PROJECT PAYMENT
# ======================================================

def add_payment(request):

    form = ProjectPaymentForm(

        request.POST or None

    )

    if form.is_valid():

        payment = form.save()

        TransactionService.create_transaction(

            source_module="Services",

            transaction_type="Income",

            reference=payment.project.project_name,

            amount=payment.amount,

            payment_mode=payment.payment_mode,

            status="Completed",

            notes=f"Project Payment - {payment.project.client.company_name}",

            user=request.user,

        )

        messages.success(

            request,

            "Payment Added Successfully."

        )

        return redirect(

            "services:service_payment_list"

        )

    return render(

        request,

        "services/add_payment.html",

        {

            "form": form

        }

    )

# ======================================================
# EDIT PROJECT PAYMENT
# ======================================================

def edit_payment(request, id):

    payment = get_object_or_404(

        ProjectPayment,

        id=id

    )

    form = ProjectPaymentForm(

        request.POST or None,

        instance=payment

    )

    if form.is_valid():

        payment = form.save()

        TransactionService.update_transaction(

            source_module="Services",

            reference=payment.project.project_name,

            amount=payment.amount,

            payment_mode=payment.payment_mode,

            status="Completed",

            notes=f"Project Payment - {payment.project.client.company_name}",

            user=request.user,

        )

        messages.success(

            request,

            "Payment Updated Successfully."

        )

        return redirect(

            "services:service_payment_list"

        )

    return render(

        request,

        "services/edit_payment.html",

        {

            "form": form,

            "payment": payment,

        }

    )

# ======================================================
# VIEW PROJECT PAYMENT
# ======================================================

def view_payment(request, id):

    payment = get_object_or_404(

        ProjectPayment,

        id=id

    )

    log_activity(

        module="Services",

        action="View",

        record_name=payment.project.project_name,

        description=f"Viewed Project Payment of ₹{payment.amount} for '{payment.project.project_name}'.",

        user=request.user,

    )

    return render(

        request,

        "services/view_payment.html",

        {

            "payment": payment,

        }

    )


# ======================================================
# DELETE PROJECT PAYMENT
# ======================================================

def delete_payment(request, id):

    payment = get_object_or_404(

        ProjectPayment,

        id=id

    )

    TransactionService.delete_transaction(

        source_module="Services",

        reference=payment.project.project_name,

        user=request.user,

    )

    payment.delete()

    messages.success(

        request,

        "Payment Deleted Successfully."

    )

    return redirect(

        "services:service_payment_list"

    )
# ======================================================
# PROJECT EXPENSE LIST
# ======================================================

def expense_list(request):

    expenses = ProjectExpense.objects.select_related(
        "project"
    ).all().order_by("-id")

    search = request.GET.get("search", "")

    if search:

        expenses = expenses.filter(

            Q(project__project_name__icontains=search) |

            Q(project__client__company_name__icontains=search) |

            Q(expense_name__icontains=search)

        )

    paginator = Paginator(expenses, 5)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    context = {

        "expenses": page_obj,

        "page_obj": page_obj,

        "search": search,

        "active_page": "expenses",

        # ===================================
        # REAL TIME SUMMARY CARDS
        # ===================================

        "total_expenses": ProjectExpense.objects.count(),

        "total_expense_amount": ProjectExpense.objects.aggregate(
            total=Sum("amount")
        )["total"] or 0,

        "today_expenses": ProjectExpense.objects.filter(
            expense_date=date.today()
        ).aggregate(
            total=Sum("amount")
        )["total"] or 0,

        "this_month_expenses": ProjectExpense.objects.filter(
            expense_date__year=date.today().year,
            expense_date__month=date.today().month
        ).aggregate(
            total=Sum("amount")
        )["total"] or 0,

    }

    return render(

        request,

        "services/expense_list.html",

        context

    )

# ======================================================
# ADD PROJECT EXPENSE
# ======================================================

def add_expense(request):

    form = ProjectExpenseForm(
        request.POST or None,
        request.FILES or None,
    )

    if request.method == "POST":

        print("POST DATA:", request.POST)

        if form.is_valid():

            print("VALID FORM")

            expense = form.save()

            messages.success(
                request,
                "Project Expense Added Successfully."
            )

            return redirect("services:expense_list")

        else:

            print("FORM ERRORS:")
            print(form.errors)
            print(form.non_field_errors())

    return render(
        request,
        "services/add_expense.html",
        {
            "form": form
        }
    )

# ======================================================
# EDIT PROJECT EXPENSE
# ======================================================

def edit_expense(request, id):

    expense = get_object_or_404(

        ProjectExpense,

        id=id

    )

    form = ProjectExpenseForm(

        request.POST or None,

        instance=expense

    )

    if form.is_valid():

        expense = form.save()

        TransactionService.update_transaction(

            source_module="Services",

            reference=expense.project.project_name,

            amount=expense.amount,

            payment_mode=expense.payment_mode,

            status="Completed",

            notes=f"Project Expense - {expense.expense_name}",

            user=request.user,

        )

        messages.success(

            request,

            "Project Expense Updated Successfully."

        )

        return redirect(

            "services:expense_list"

        )

    return render(

        request,

        "services/edit_expense.html",

        {

            "form": form,

            "expense": expense,

        }

    )


# ======================================================
# VIEW PROJECT EXPENSE
# ======================================================

def view_expense(request, id):

    expense = get_object_or_404(

        ProjectExpense,

        id=id

    )

    log_activity(

        module="Services",

        action="View",

        record_name=expense.project.project_name,

        description=f"Viewed Project Expense '{expense.expense_name}' (₹{expense.amount}) for project '{expense.project.project_name}'.",

        user=request.user,

    )

    return render(

        request,

        "services/view_expense.html",

        {

            "expense": expense,

        }

    )


# ======================================================
# DELETE PROJECT EXPENSE
# ======================================================

def delete_expense(request, id):

    expense = get_object_or_404(

        ProjectExpense,

        id=id

    )

    TransactionService.delete_transaction(

        source_module="Services",

        reference=expense.project.project_name,

        user=request.user,

    )

    expense.delete()

    messages.success(

        request,

        "Project Expense Deleted Successfully."

    )

    return redirect(

        "services:expense_list"

    )

# ======================================================
# EMPLOYEE SALARY LIST
# ======================================================

def salary_list(request):

    salaries = EmployeeSalary.objects.select_related(
        "project"
    ).all().order_by("-id")

    search = request.GET.get("search")

    if search:

        salaries = salaries.filter(

            Q(employee_name__icontains=search) |

            Q(project__project_name__icontains=search)

        )

    total_employees = salaries.count()

    total_salary = salaries.aggregate(
        Sum("net_salary")
    )["net_salary__sum"] or 0

    paid_salary = salaries.filter(
        payment_status="Paid"
    ).aggregate(
        Sum("net_salary")
    )["net_salary__sum"] or 0

    pending_salary = salaries.filter(
        payment_status="Pending"
    ).aggregate(
        Sum("net_salary")
    )["net_salary__sum"] or 0

    paginator = Paginator(salaries, 5)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(

        request,

        "services/salary_list.html",

        {

            "salaries": page_obj,

            "page_obj": page_obj,

            "search": search,

            "active_page": "salary",

            "total_employees": total_employees,

            "total_salary": total_salary,

            "paid_salary": paid_salary,

            "pending_salary": pending_salary,

        }

    )

# ======================================================
# ADD EMPLOYEE SALARY
# ======================================================



def add_salary(request):

    form = EmployeeSalaryForm(
        request.POST or None
    )

    if request.method == "POST":

        print("POST DATA:", request.POST)

        if form.is_valid():

            print("VALID FORM")

            salary = form.save()

            TransactionService.create_transaction(

                source_module="Services",

                transaction_type="Expense",

                reference=salary.employee_name,

                amount=salary.net_salary,

                payment_mode=salary.payment_mode,

                status=salary.payment_status,

                notes=f"Employee Salary - {salary.employee_name}",

                user=request.user,

            )

            messages.success(
                request,
                "Employee Salary Added Successfully."
            )

            return redirect("services:salary_list")

        else:

            print("FORM ERRORS:")
            print(form.errors)

    return render(

        request,

        "services/add_salary.html",

        {
            "form": form,
        }

    )

# ======================================================
# EDIT EMPLOYEE SALARY
# ======================================================

def edit_salary(request, id):

    salary = get_object_or_404(

        EmployeeSalary,

        id=id

    )

    form = EmployeeSalaryForm(

        request.POST or None,

        instance=salary

    )

    if form.is_valid():

        salary = form.save()

        TransactionService.update_transaction(

            source_module="Services",

            reference=salary.employee_name,

            amount=salary.net_salary,

            payment_mode=salary.payment_mode,

            status=salary.payment_status,

            notes=f"Employee Salary - {salary.employee_name}",

            user=request.user,

        )

        messages.success(

            request,

            "Employee Salary Updated Successfully."

        )

        return redirect(

            "services:salary_list"

        )

    return render(

        request,

        "services/edit_salary.html",

        {

            "form": form,

            "salary": salary,

        }

    )

# ======================================================
# VIEW EMPLOYEE SALARY
# ======================================================

def view_salary(request, id):

    salary = get_object_or_404(

        EmployeeSalary,

        id=id

    )

    log_activity(

        module="Services",

        action="View",

        record_name=salary.employee_name,

        description=f"Viewed Employee Salary of '{salary.employee_name}' (₹{salary.net_salary}).",

        user=request.user,

    )

    return render(

        request,

        "services/view_salary.html",

        {

            "salary": salary,

        }

    )


# ======================================================
# DELETE EMPLOYEE SALARY
# ======================================================

def delete_salary(request, id):

    salary = get_object_or_404(

        EmployeeSalary,

        id=id

    )

    TransactionService.delete_transaction(

        source_module="Services",

        reference=salary.employee_name,

        user=request.user,

    )

    salary.delete()

    messages.success(

        request,

        "Employee Salary Deleted Successfully."

    )

    return redirect(

        "services:salary_list"

    )
    
def salary_export_excel(request):

    workbook = Workbook()

    worksheet = workbook.active

    worksheet.title = "Employee Salary"

    worksheet.append([
        "Employee ID",
        "Employee Name",
        "Project",
        "Salary Month",
        "Basic Salary",
        "Bonus",
        "Deduction",
        "Net Salary",
        "Payment Status"
    ])

    salaries = EmployeeSalary.objects.select_related(
        "project"
    ).all().order_by("-id")

    for salary in salaries:

        worksheet.append([
            salary.employee_id,
            salary.employee_name,
            salary.project.project_name,
            str(salary.salary_month),
            salary.basic_salary,
            salary.bonus,
            salary.deduction,
            salary.net_salary,
            salary.payment_status,
        ])

    response = HttpResponse(

        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    )

    response["Content-Disposition"] = (

        'attachment; filename="employee_salary.xlsx"'

    )

    workbook.save(response)

    return response

def salary_export_pdf(request):

    response = HttpResponse(content_type="application/pdf")

    response["Content-Disposition"] = 'attachment; filename="employee_salary.pdf"'

    doc = SimpleDocTemplate(response)

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph(
        "<b>Employee Salary Report</b>",
        styles["Heading1"]
    )

    elements.append(title)

    elements.append(Paragraph("<br/>", styles["Normal"]))

    data = [[
        "Emp ID",
        "Employee",
        "Project",
        "Month",
        "Basic",
        "Bonus",
        "Deduction",
        "Net Salary",
        "Status"
    ]]

    salaries = EmployeeSalary.objects.select_related(
        "project"
    ).all().order_by("-id")

    for salary in salaries:

        data.append([

            salary.employee_id,

            salary.employee_name,

            salary.project.project_name,

            str(salary.salary_month),

            f"₹{salary.basic_salary}",

            f"₹{salary.bonus}",

            f"₹{salary.deduction}",

            f"₹{salary.net_salary}",

            salary.payment_status,

        ])

    table = Table(data)

    table.setStyle(TableStyle([

        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#198754")),

        ("TEXTCOLOR", (0,0), (-1,0), colors.white),

        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),

        ("FONTSIZE", (0,0), (-1,-1), 10),

        ("BOTTOMPADDING", (0,0), (-1,0), 10),

        ("BACKGROUND", (0,1), (-1,-1), colors.beige),

        ("GRID", (0,0), (-1,-1), 1, colors.grey),

        ("ALIGN", (0,0), (-1,-1), "CENTER"),

        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),

    ]))

    elements.append(table)

    doc.build(elements)

    return response