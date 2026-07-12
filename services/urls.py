from django.urls import path
from . import views

app_name = "services"

urlpatterns = [

    # Services Home
    path(
        "",
        views.client_list,
        name="services_home"
    ),

    # CLIENTS
    path("clients/", views.client_list, name="client_list"),
    path("clients/add/", views.add_client, name="add_client"),
    path("clients/edit/<int:id>/", views.edit_client, name="edit_client"),
    path("clients/view/<int:id>/", views.view_client, name="view_client"),
    path("clients/delete/<int:id>/", views.delete_client, name="delete_client"),

    # PROJECTS
    path("projects/", views.project_list, name="project_list"),
    path("projects/add/", views.add_project, name="add_project"),
    path("projects/edit/<int:id>/", views.edit_project, name="edit_project"),
    path("projects/view/<int:id>/", views.view_project, name="view_project"),
    path("projects/delete/<int:id>/", views.delete_project, name="delete_project"),
    
    # =====================================
    # PROJECT PAYMENTS
    # =====================================

    path("payments/", views.payment_list, name="service_payment_list"),

    path(
        "payments/add/",
        views.add_payment,
        name="add_payment"
    ),

    path(
        "payments/edit/<int:id>/",
        views.edit_payment,
        name="edit_payment"
    ),

    path(
        "payments/view/<int:id>/",
        views.view_payment,
        name="view_payment"
    ),

    path(
        "payments/delete/<int:id>/",
        views.delete_payment,
        name="delete_payment"
    ),
    # =====================================
    # PROJECT EXPENSES
    # =====================================

    path(
        "project-expenses/",
        views.expense_list,
        name="expense_list"
    ),

    path(
        "project-expenses/add/",
        views.add_expense,
        name="add_expense"
    ),

    path(
        "project-expenses/edit/<int:id>/",
        views.edit_expense,
        name="edit_expense"
    ),

    path(
        "project-expenses/view/<int:id>/",
        views.view_expense,
        name="view_expense"
    ),

    path(
        "project-expenses/delete/<int:id>/",
        views.delete_expense,
        name="delete_expense"
    ),
    
    # ======================================================
    # EMPLOYEE SALARY
    # ======================================================

    path(
        "salary/",
        views.salary_list,
        name="salary_list",
    ),

    path(
        "salary/add/",
        views.add_salary,
        name="add_salary",
    ),

    path(
        "salary/edit/<int:id>/",
        views.edit_salary,
        name="edit_salary",
    ),

    path(
        "salary/view/<int:id>/",
        views.view_salary,
        name="view_salary",
    ),

    path(
        "salary/delete/<int:id>/",
        views.delete_salary,
        name="delete_salary",
    ),
    path(
        "salary/export/excel/",
        views.salary_export_excel,
        name="salary_export_excel",
    ),
    path(
        "salary/export/pdf/",
        views.salary_export_pdf,
        name="salary_export_pdf",
    ),
]