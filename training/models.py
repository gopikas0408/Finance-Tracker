from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
import re
from django.db.models import Sum


# =====================================================
# COURSE MODEL
# =====================================================

class Course(models.Model):

    MODE_CHOICES = (
        ("Online", "Online"),
        ("Offline", "Offline"),
        ("Hybrid", "Hybrid"),
    )

    STATUS_CHOICES = (
        ("Active", "Active"),
        ("Inactive", "Inactive"),
    )

    course_name = models.CharField(
        max_length=200
    )

    duration = models.CharField(
        max_length=100
    )

    course_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    trainer_name = models.CharField(
        max_length=150
    )

    training_mode = models.CharField(
        max_length=20,
        choices=MODE_CHOICES,
        default="Offline"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Active"
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = ["-id"]

    def clean(self):

        # Course Name
        if len(self.course_name.strip()) < 3:

            raise ValidationError({
                "course_name":
                "Course name must contain at least 3 characters."
            })

        if not re.match(
            r"^[A-Za-z0-9 &()-.]+$",
            self.course_name
        ):

            raise ValidationError({
                "course_name":
                "Invalid course name."
            })

        # Duration
        if len(self.duration.strip()) < 2:

            raise ValidationError({
                "duration":
                "Enter a valid duration."
            })

        # Course Fee
        if self.course_fee <= 0:

            raise ValidationError({
                "course_fee":
                "Course fee must be greater than zero."
            })

        # Trainer Name
        if len(self.trainer_name.strip()) < 3:

            raise ValidationError({
                "trainer_name":
                "Trainer name is too short."
            })

        if not re.match(
            r"^[A-Za-z ]+$",
            self.trainer_name
        ):

            raise ValidationError({
                "trainer_name":
                "Trainer name should contain only letters."
            })

        # Description
        if self.description and len(self.description) > 500:

            raise ValidationError({
                "description":
                "Description cannot exceed 500 characters."
            })

    def save(self, *args, **kwargs):

        self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self):

        return self.course_name


# =====================================================
# STUDENT MODEL
# =====================================================

class Student(models.Model):

    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )

    trainer_name = models.CharField(
        max_length=100,
        blank=True
    )

    course_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    

    STATUS_CHOICES = (
        ("Pending Payment", "Pending Payment"),
        ("Partial Payment", "Partial Payment"),
        ("Paid", "Paid"),
    )

    student_name = models.CharField(
        max_length=200
    )

    email = models.EmailField(
        unique=True
    )

    phone = models.CharField(
        max_length=15,
        unique=True
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    date_of_birth = models.DateField()

    address = models.TextField()

    photo = models.ImageField(
        upload_to="students/",
        blank=True,
        null=True
    )


    admission_date = models.DateField()


    



    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="Pending Payment"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = ["-id"]

    # ==========================================
    # VALIDATION
    # ==========================================

    def clean(self):

        # Student Name

        if len(self.student_name.strip()) < 3:

            raise ValidationError({

                "student_name":
                "Student name must contain at least 3 characters."

            })

        if not re.match(
            r"^[A-Za-z ]+$",
            self.student_name
        ):

            raise ValidationError({

                "student_name":
                "Student name should contain only letters."

            })

        # Phone

        if not self.phone.isdigit():

            raise ValidationError({

                "phone":
                "Phone number must contain only digits."

            })

        if len(self.phone) != 10:

            raise ValidationError({

                "phone":
                "Phone number must contain exactly 10 digits."

            })

        # Age

        today = timezone.now().date()

        age = today.year - self.date_of_birth.year - (
            (today.month, today.day)
            <
            (self.date_of_birth.month, self.date_of_birth.day)
        )

        if age < 15:

            raise ValidationError({

                "date_of_birth":
                "Student must be at least 15 years old."

            })

        # Admission Date

        if self.admission_date > today:

            raise ValidationError({

                "admission_date":
                "Admission date cannot be in the future."

            })

        

        # Address

        if self.address and len(self.address) > 500:

            raise ValidationError({

                "address":
                "Address cannot exceed 500 characters."

            })

    # ==========================================
    # SAVE
    # ==========================================

    def save(self, *args, **kwargs):

        if self.course:

            self.course_fee = self.course.course_fee

            self.trainer_name = self.course.trainer_name

        # Only when creating a new student
        if not self.pk:

            self.paid_amount = 0

            self.balance_amount = self.course_fee

            self.status = "Pending Payment"

        super().save(*args, **kwargs)

    def __str__(self):

        return f"{self.student_name} - {self.course.course_name}"
    
# =====================================================
# STUDENT PAYMENT MODEL
# =====================================================

class StudentPayment(models.Model):

    PAYMENT_MODE = (
        ("Cash", "Cash"),
        ("UPI", "UPI"),
        ("Bank", "Bank"),
        ("Card", "Card"),
    )
  

    transaction_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    cheque_number = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    bank_name = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_mode = models.CharField(
        max_length=20,
        choices=PAYMENT_MODE
    )

    payment_date = models.DateField()

    remarks = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = ["-id"]

    # ==========================================
    # VALIDATION
    # ==========================================

    def clean(self):

        # Student

        if not self.student:

            raise ValidationError({

                "student":
                "Please select a student."

            })

        # Amount

        if self.amount <= 0:

            raise ValidationError({

                "amount":
                "Amount must be greater than zero."

            })

        # Payment Date

        

        if self.payment_date > timezone.localdate():
            raise ValidationError({
                "payment_date": "Future Date is not allowed."
            })
            
        # ==========================================
        # Payment Mode Validation
        # ==========================================

        


        elif self.payment_mode in ["UPI", "Bank", "Card"]:

            if not self.transaction_id:

                raise ValidationError({
                    "transaction_id":
                    "Transaction ID is required."
                })


        elif self.payment_mode == "Cheque":

            if not self.cheque_number:

                raise ValidationError({
                    "cheque_number":
                    "Cheque Number is required."
                })

            if not self.bank_name:

                raise ValidationError({
                    "bank_name":
                    "Bank Name is required."
                })

        # Remarks

        if self.remarks and len(self.remarks) > 500:

            raise ValidationError({

                "remarks":
                "Remarks cannot exceed 500 characters."

            })

        

        # Paid amount should not exceed course fee

        total_paid = (
            StudentPayment.objects.filter(student=self.student)
            .exclude(pk=self.pk)
            .aggregate(total=Sum("amount"))["total"] or 0
        )

        total_paid += self.amount

        if total_paid > self.student.course_fee:

            raise ValidationError({

                "amount": "Payment exceeds the remaining balance."

            })

    # ==========================================
    # SAVE
    # ==========================================

    def save(self, *args, **kwargs):

        self.full_clean()

        old_amount = 0

        if self.pk:

            old_amount = StudentPayment.objects.get(
                pk=self.pk
            ).amount

        super().save(*args, **kwargs)

        total_paid = sum(

            payment.amount

            for payment in self.student.payments.all()

        )

        self.student.paid_amount = total_paid

        self.student.balance_amount = (

            self.student.course_fee -

            total_paid

        )

        self.student.save()

    # ==========================================
    # DELETE
    # ==========================================

    def delete(self, *args, **kwargs):

        student = self.student

        super().delete(*args, **kwargs)

        total_paid = sum(

            payment.amount

            for payment in student.payments.all()

        )

        student.paid_amount = total_paid

        student.balance_amount = (

            student.course_fee -

            total_paid

        )

        student.save()

    def __str__(self):

        return f"{self.student.student_name} - ₹{self.amount}"
    
class StudentPaymentCashDenomination(models.Model):

    DENOMINATION_CHOICES = (

        ("500", "₹500"),
        ("200", "₹200"),
        ("100", "₹100"),
        ("50", "₹50"),
        ("20", "₹20"),
        ("10", "₹10"),
        

    )

    payment = models.ForeignKey(

        StudentPayment,

        on_delete=models.CASCADE,

        related_name="cash_denominations"

    )

    denomination = models.CharField(

        max_length=20,

        choices=DENOMINATION_CHOICES

    )

    custom_denomination = models.PositiveIntegerField(

        blank=True,

        null=True

    )

    notes_count = models.PositiveIntegerField()

    amount = models.DecimalField(

        max_digits=12,

        decimal_places=2,

        editable=False,

        default=0

    )

    def clean(self):

        if self.denomination == "Others":

            if not self.custom_denomination:

                raise ValidationError({

                    "custom_denomination":
                    "Enter custom denomination."

                })

            value = self.custom_denomination

        else:

            if self.denomination == "Coins":

                value = 1

            else:

                value = int(self.denomination)

        self.amount = value * self.notes_count

    def save(self, *args, **kwargs):

        self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self):

        return f"{self.denomination} x {self.notes_count}"