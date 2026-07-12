from django.urls import path
from . import views

urlpatterns = [
    
    # Training Home
    path(
        "",
        views.training_home,
        name="training_home"
    ),


    # =====================================================
    # COURSE MANAGEMENT
    # =====================================================

    path(
        "courses/",
        views.course_list,
        name="course_list"
    ),

    path(
        "courses/add/",
        views.add_course,
        name="add_course"
    ),

    path(
        "courses/edit/<int:id>/",
        views.edit_course,
        name="edit_course"
    ),

    path(
        "courses/view/<int:id>/",
        views.view_course,
        name="view_course"
    ),

    path(
        "courses/delete/<int:id>/",
        views.delete_course,
        name="delete_course"
    ),

    # =====================================================
    # STUDENT MANAGEMENT
    # =====================================================

    path(
        "students/",
        views.student_list,
        name="student_list"
    ),

    path(
        "students/add/",
        views.add_student,
        name="add_student"
    ),

    path(
        "students/edit/<int:id>/",
        views.edit_student,
        name="edit_student"
    ),

    path(
        "students/view/<int:id>/",
        views.view_student,
        name="view_student"
    ),

    path(
        "students/delete/<int:id>/",
        views.delete_student,
        name="delete_student"
    ),

    # =====================================================
    # STUDENT PAYMENT MANAGEMENT
    # =====================================================

    path(
        "payments/",
        views.payment_list,
        name="payment_list"
    ),

    path(
        "payments/add/",
        views.add_payment,
        name="add_payment"
    ),
    path(
        "student-fee/<int:student_id>/",
        views.get_student_fee_details,
        name="student_fee_details"
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

]

