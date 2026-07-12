from django.urls import path
from . import views

urlpatterns = [

    # ===========================================
    # TRANSACTION LIST
    # ===========================================

    path(

        "",

        views.transaction_list,

        name="transaction_list",

    ),

    # ===========================================
    # VIEW TRANSACTION
    # ===========================================

    path(

        "view/<int:id>/",

        views.view_transaction,

        name="view_transaction",

    ),

    # ===========================================
    # EXPORT EXCEL
    # ===========================================

    path(

        "export/excel/",

        views.export_transaction_excel,

        name="export_transaction_excel",

    ),

    # ===========================================
    # EXPORT PDF
    # ===========================================

    path(

        "export/pdf/",

        views.export_transaction_pdf,

        name="export_transaction_pdf",

    ),

]