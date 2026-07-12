from django.urls import path
from . import views

app_name = "expenses"

urlpatterns = [

    path("", views.expense_list, name="expense_list"),

    path("add/", views.add_expense, name="add_expense"),

    path("edit/<int:id>/", views.edit_expense, name="edit_expense"),

    path("view/<int:id>/", views.view_expense, name="view_expense"),

    path("delete/<int:id>/", views.delete_expense, name="delete_expense"),

    path("export/excel/", views.export_expense_excel, name="export_expense_excel"),

    path("export/pdf/", views.export_expense_pdf, name="export_expense_pdf"),

]