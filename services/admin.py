from django.contrib import admin
from .models import Client, Project, ProjectPayment, ProjectExpense


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):

    list_display = (
        "company_name",
        "contact_person",
        "phone",
        "email",
        "status",
    )

    search_fields = (
        "company_name",
        "contact_person",
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):

    list_display = (
        "project_name",
        "client",
        "service_type",
        "project_amount",
        "status",
    )

    list_filter = (
        "service_type",
        "status",
    )

    search_fields = (
        "project_name",
        "client__company_name",
    )


@admin.register(ProjectPayment)
class ProjectPaymentAdmin(admin.ModelAdmin):

    list_display = (
        "project",
        "amount",
        "payment_mode",
        "payment_date",
    )

    list_filter = (
        "payment_mode",
        "payment_date",
    )

    search_fields = (
        "project__project_name",
    )


@admin.register(ProjectExpense)
class ProjectExpenseAdmin(admin.ModelAdmin):

    list_display = (
        "project",
        "expense_name",
        "amount",
        "expense_date",
    )

    list_filter = (
        "expense_date",
    )

    search_fields = (
        "project__project_name",
        "expense_name",
    )
    
from .models import EmployeeSalary

admin.site.register(EmployeeSalary)