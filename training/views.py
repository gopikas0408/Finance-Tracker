from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Student, StudentPayment
from .forms import CourseForm, StudentForm, StudentPaymentForm

from django.contrib import messages

from activity.services import (
    create_notification,
    log_activity,
)
from .forms import (
    StudentPaymentForm,
    StudentPaymentCashDenominationFormSet,
)
from transactions.services import TransactionService

from activity.models import Achievement
from django.db.models import Sum

def training_home(request):

    return redirect("course_list")

def course_list(request):

    courses = Course.objects.all()

    context = {

        "courses": courses,

        "total_courses": courses.count(),

        "active_courses": courses.filter(status="Active").count(),

        "inactive_courses": courses.filter(status="Inactive").count(),

        "active_page": "courses",

    }

    return render(

        request,

        "training/course_list.html",

        context

    )


def add_course(request):

    form = CourseForm(request.POST or None)

    if form.is_valid():

        course = form.save()

        create_notification(

            title="Course Added",

            message=f"{course.course_name} course created successfully.",

            module="Training",

            action="Add",

            priority="Medium",

            user=request.user,

        )

        log_activity(

            module="Training",

            action="Add",

            record_name=course.course_name,

            description=f"New course '{course.course_name}' added.",

            user=request.user,

        )

        messages.success(

            request,

            "Course Added Successfully."

        )

        return redirect("course_list")

    return render(

        request,

        "training/add_course.html",

        {

            "form": form,

            "active_page": "courses",

        }

    )


def edit_course(request, id):

    course = get_object_or_404(

        Course,

        id=id

    )

    form = CourseForm(

        request.POST or None,

        instance=course

    )

    if form.is_valid():

        course = form.save()

        create_notification(

            title="Course Updated",

            message=f"{course.course_name} updated successfully.",

            module="Training",

            action="Edit",

            priority="Low",

            user=request.user,

        )

        log_activity(

            module="Training",

            action="Edit",

            record_name=course.course_name,

            description=f"Course '{course.course_name}' updated.",

            user=request.user,

        )

        messages.success(

            request,

            "Course Updated Successfully."

        )

        return redirect("course_list")

    return render(

        request,

        "training/edit_course.html",

        {

            "form": form,

            "course": course,

            "active_page": "courses",

        }

    )


def view_course(request, id):

    course = get_object_or_404(

        Course,

        id=id

    )

    log_activity(

        module="Training",

        action="View",

        record_name=course.course_name,

        description="Viewed course details.",

        user=request.user,

    )

    return render(

        request,

        "training/view_course.html",

        {

            "course": course,

            "active_page": "courses",

        }

    )


def delete_course(request, id):

    course = get_object_or_404(

        Course,

        id=id

    )

    create_notification(

        title="Course Deleted",

        message=f"{course.course_name} deleted.",

        module="Training",

        action="Delete",

        priority="High",

        user=request.user,

    )

    log_activity(

        module="Training",

        action="Delete",

        record_name=course.course_name,

        description=f"Course '{course.course_name}' deleted.",

        user=request.user,

    )

    course.delete()

    messages.success(

        request,

        "Course Deleted Successfully."

    )

    return redirect("course_list")


# =====================================================
# STUDENT MANAGEMENT
# =====================================================

def student_list(request):

    students = Student.objects.select_related("course").all()

    search = request.GET.get("search")

    if search:

        students = students.filter(

            student_name__icontains=search

        )

    context = {

        "students": students,

        "search": search,

        "total_students": students.count(),

        "active_students": students.filter(
            status="Active"
        ).count(),

        "completed_students": students.filter(
            status="Completed"
        ).count(),


        "active_page": "students",

    }

    return render(

        request,

        "training/student_list.html",

        context

    )


def add_student(request):

    form = StudentForm(

        request.POST or None,

        request.FILES or None

    )

    if form.is_valid():

        student = form.save()

        create_notification(

            title="Student Registered",

            message=f"{student.student_name} enrolled in {student.course.course_name}.",

            module="Training",

            action="Add",

            priority="Medium",

            user=request.user,

        )

        log_activity(

            module="Training",

            action="Add",

            record_name=student.student_name,

            description=f"Student registered for {student.course.course_name}.",

            user=request.user,

        )

        messages.success(

            request,

            "Student Added Successfully."

        )

        return redirect("student_list")

    return render(

        request,

        "training/add_student.html",

        {

            "form": form,

            "active_page": "students",

        }

    )


def edit_student(request, id):

    student = get_object_or_404(

        Student,

        id=id

    )

    form = StudentForm(

        request.POST or None,

        request.FILES or None,

        instance=student

    )

    if form.is_valid():

        student = form.save()

        create_notification(

            title="Student Updated",

            message=f"{student.student_name} details updated.",

            module="Training",

            action="Edit",

            priority="Low",

            user=request.user,

        )

        log_activity(

            module="Training",

            action="Edit",

            record_name=student.student_name,

            description="Student details updated.",

            user=request.user,

        )

        messages.success(

            request,

            "Student Updated Successfully."

        )

        return redirect("student_list")

    return render(

        request,

        "training/edit_student.html",

        {

            "form": form,

            "student": student,

            "active_page": "students",

        }

    )


def view_student(request, id):

    student = get_object_or_404(

        Student,

        id=id

    )

    log_activity(

        module="Training",

        action="View",

        record_name=student.student_name,

        description="Viewed student profile.",

        user=request.user,

    )

    return render(

        request,

        "training/view_student.html",

        {

            "student": student,

            "active_page": "students",

        }

    )


def delete_student(request, id):

    student = get_object_or_404(

        Student,

        id=id

    )

    create_notification(

        title="Student Deleted",

        message=f"{student.student_name} removed from the course.",

        module="Training",

        action="Delete",

        priority="High",

        user=request.user,

    )

    log_activity(

        module="Training",

        action="Delete",

        record_name=student.student_name,

        description="Student deleted from the system.",

        user=request.user,

    )

    student.delete()

    messages.success(

        request,

        "Student Deleted Successfully."

    )

    return redirect("student_list")

# =====================================================
# STUDENT PAYMENT MANAGEMENT
# =====================================================

def payment_list(request):

    payments = StudentPayment.objects.select_related(
        "student",
        "student__course"
    ).all().order_by("-id")
    
    for payment in payments:

        total_paid = (
            StudentPayment.objects.filter(
                student=payment.student
            ).aggregate(
                total=Sum("amount")
            )["total"] or 0
        )

        payment.total_paid = total_paid
        payment.balance = payment.student.course_fee - total_paid

    search = request.GET.get("search")

    if search:

        payments = payments.filter(

            student__student_name__icontains=search

        )

    context = {

        "payments": payments,

        "search": search,

        "total_payments": payments.count(),

        "total_amount": sum(

            payment.amount

            for payment in payments

        ),

        "active_page": "payments",

    }

    return render(

        request,

        "training/payment_list.html",

        context

    )


# ======================================================
# ADD STUDENT PAYMENT
# ======================================================

def add_payment(request):

    form = StudentPaymentForm(request.POST or None)

    formset = AddStudentPaymentCashDenominationFormSet(
        request.POST or None
    )

    if form.is_valid() and formset.is_valid():
        payment = form.save()
        
        denominations = formset.save(commit=False)

        for denomination in denominations:

            denomination.payment = payment

            denomination.save()

        student = payment.student

        # ==========================================
        # TOTAL PAID & BALANCE
        # ==========================================

        total_paid = (
            StudentPayment.objects.filter(
                student=student
            ).aggregate(
                total=Sum("amount")
            )["total"] or 0
        )

        balance = student.course_fee - total_paid

        # ==========================================
        # STUDENT STATUS
        # ==========================================

        if balance <= 0:

            student.status = "Completed"

            # ======================================
            # ACHIEVEMENT
            # ======================================

            Achievement.objects.get_or_create(

                title="Student Fee Collection Completed",

                defaults={

                    "description":
                    f"{student.student_name} has successfully completed the course fee payment."

                }

            )

        else:

            student.status = "Active"

        student.save(update_fields=["status"])

        # ==========================================
        # CREATE TRANSACTION
        # ==========================================

        TransactionService.create_transaction(

            source_module="Training",

            transaction_type="Income",

            reference=student.student_name,

            amount=payment.amount,

            payment_mode=payment.payment_mode,

            status="Completed",

            notes=f"Student Fee Payment - {student.student_name}",

            user=request.user,

        )

        messages.success(

            request,

            "Payment Added Successfully."

        )

        return redirect("payment_list")

    return render(

        request,

        "training/add_payment.html",

        {

            "form": form,
            
            "formset": formset,

            "active_page": "payments",

        }

    )


# ======================================================
# EDIT STUDENT PAYMENT
# ======================================================

def edit_payment(request, id):

    payment = get_object_or_404(

        StudentPayment,

        id=id

    )

    form = StudentPaymentForm(

        request.POST or None,

        instance=payment

    )
    formset = StudentPaymentCashDenominationFormSet(
        request.POST or None,
        instance=payment
    )

    if form.is_valid() and formset.is_valid():

        payment = form.save()
        formset.instance = payment

        formset.save()

        student = payment.student

        total_paid = (
            StudentPayment.objects.filter(
                student=student
            ).aggregate(
                total=Sum("amount")
            )["total"] or 0
        )

        balance = student.course_fee - total_paid

        if balance <= 0:
            student.status = "Completed"
        else:
            student.status = "Active"

        student.save(update_fields=["status"])

        TransactionService.update_transaction(

            source_module="Training",

            reference=student.student_name,

            amount=payment.amount,

            payment_mode=payment.payment_mode,

            status="Completed",

            notes=f"Student Fee Payment - {student.student_name}",

            user=request.user,

        )

        messages.success(

            request,

            "Payment Updated Successfully."

        )

        return redirect("payment_list")

    return render(

        request,

        "training/edit_payment.html",

        {

            "form": form,
            
            "formset": formset,

            "payment": payment,

            "active_page": "payments",

        }

    )


# ======================================================
# VIEW STUDENT PAYMENT
# ======================================================

def view_payment(request, id):

    payment = get_object_or_404(

        StudentPayment,

        id=id

    )

    log_activity(

        module="Training",

        action="View",

        record_name=payment.student.student_name,

        description=f"Viewed Student Payment of ₹{payment.amount} for '{payment.student.student_name}'.",

        user=request.user,

    )

    return render(

        request,

        "training/view_payment.html",

        {

            "payment": payment,
            
            "cash_denominations": payment.cash_denominations.all(),

            "active_page": "payments",

        }

    )


# ======================================================
# DELETE STUDENT PAYMENT
# ======================================================

def delete_payment(request, id):

    payment = get_object_or_404(

        StudentPayment,

        id=id

    )

    TransactionService.delete_transaction(

        source_module="Training",

        reference=payment.student.student_name,

        user=request.user,

    )

    payment.delete()

    messages.success(

        request,

        "Payment Deleted Successfully."

    )

    return redirect(

        "payment_list"

    )
    
    
from django.db.models import Sum

def get_student_fee_details(request, student_id):

    try:
        student = Student.objects.get(id=student_id)

        paid = StudentPayment.objects.filter(
            student=student
        ).aggregate(
            total=Sum("amount")
        )["total"] or 0

        balance = student.course_fee - paid

        return JsonResponse({
            "course_fee": float(student.course_fee),
            "paid_amount": float(paid),
            "balance_amount": float(balance),
        })

    except Student.DoesNotExist:
        return JsonResponse({"error": "Student not found"}, status=404)