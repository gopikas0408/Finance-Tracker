from django.contrib import admin
from .models import Course, Student, StudentPayment


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    list_display = (
        "course_name",
        "duration",
        "course_fee",
        "trainer_name",
        "training_mode",
        "status",
    )

    search_fields = (
        "course_name",
        "trainer_name",
    )

    list_filter = (
        "training_mode",
        "status",
    )

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):

    list_display = (
        "student_name",
        "course",
        "phone",
        "status",
    )

    search_fields = (
        "student_name",
        "email",
        "phone",
    )

    list_filter = (
        "course",
        "status",
    )
    
@admin.register(StudentPayment)
class StudentPaymentAdmin(admin.ModelAdmin):

    list_display = (

        "student",

        "amount",

        "payment_mode",

        "payment_date",

    )

    search_fields = (

        "student__student_name",

    )