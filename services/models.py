from django.db import models


# ==========================================
# CLIENT MODEL
# ==========================================


from django.core.exceptions import ValidationError
import re


class Client(models.Model):

    STATUS_CHOICES = (
        ("Active", "Active"),
        ("Inactive", "Inactive"),
    )

    company_name = models.CharField(
        max_length=200
    )

    contact_person = models.CharField(
        max_length=150
    )

    phone = models.CharField(
        max_length=10,
        unique=True
    )

    email = models.EmailField(
        unique=True
    )

    address = models.TextField(
        blank=True,
        null=True
    )

    gst_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        unique=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Active"
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

        if len(self.company_name.strip()) < 3:

            raise ValidationError({

                "company_name":

                "Company name must contain at least 3 characters."

            })

        if not re.match(

            r'^[A-Za-z0-9&().,\- ]+$',

            self.company_name

        ):

            raise ValidationError({

                "company_name":

                "Invalid company name."

            })

        if not re.match(

            r'^[A-Za-z ]+$',

            self.contact_person

        ):

            raise ValidationError({

                "contact_person":

                "Only alphabets are allowed."

            })

        if not re.match(

            r'^[6-9]\d{9}$',

            self.phone

        ):

            raise ValidationError({

                "phone":

                "Phone number must contain exactly 10 digits."

            })

        if self.gst_number:

            gst = self.gst_number.upper()

            pattern = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][1-9A-Z]Z[0-9A-Z]$'

            if not re.match(pattern, gst):

                raise ValidationError({

                    "gst_number":

                    "Enter a valid GST Number."

                })

    def __str__(self):

        return self.company_name


# ==========================================
# PROJECT MODEL
# ==========================================

from django.core.exceptions import ValidationError
from django.utils import timezone
import re


class Project(models.Model):

    SERVICE_CHOICES = (

        ("Website", "Website"),
        ("Web Application", "Web Application"),
        ("Mobile Application", "Mobile Application"),
        ("UI/UX Design", "UI/UX Design"),
        ("Digital Marketing", "Digital Marketing"),
        ("SEO", "SEO"),
        ("ERP Development", "ERP Development"),
        ("Other", "Other"),

    )

    STATUS_CHOICES = (

        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
        ("On Hold", "On Hold"),

    )

    client = models.ForeignKey(

        Client,

        on_delete=models.CASCADE,

        related_name="projects"

    )

    project_name = models.CharField(

        max_length=200,

        unique=True

    )

    service_type = models.CharField(

        max_length=100,

        choices=SERVICE_CHOICES

    )

    project_amount = models.DecimalField(

        max_digits=12,

        decimal_places=2

    )

    start_date = models.DateField()

    end_date = models.DateField()

    status = models.CharField(

        max_length=30,

        choices=STATUS_CHOICES,

        default="Pending"

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

    # ==========================================
    # MODEL VALIDATION
    # ==========================================

    def clean(self):

        # Project Name

        if len(self.project_name.strip()) < 3:

            raise ValidationError({

                "project_name":

                "Project name must contain at least 3 characters."

            })

        if not re.match(

            r'^[A-Za-z0-9&().,_\- ]+$',

            self.project_name

        ):

            raise ValidationError({

                "project_name":

                "Project name contains invalid characters."

            })

        # Amount

        if self.project_amount <= 0:

            raise ValidationError({

                "project_amount":

                "Project amount must be greater than zero."

            })

        # Start Date

        if self.start_date > timezone.now().date():

            raise ValidationError({

                "start_date":

                "Future start date is not allowed."

            })

        # End Date

        if self.end_date < self.start_date:

            raise ValidationError({

                "end_date":

                "End date must be after Start Date."

            })

        # Description

        if self.description:

            if len(self.description) > 500:

                raise ValidationError({

                    "description":

                    "Description cannot exceed 500 characters."

                })

    def __str__(self):

        return self.project_name
# ==========================================
# PROJECT PAYMENT MODEL
# ==========================================

from django.core.exceptions import ValidationError
from django.utils import timezone


class ProjectPayment(models.Model):

    PAYMENT_MODE = (

        ("Cash", "Cash"),
        ("UPI", "UPI"),
        ("Bank", "Bank"),
        ("Card", "Card"),

    )

    project = models.ForeignKey(

        Project,

        on_delete=models.CASCADE

    )

    amount = models.DecimalField(

        max_digits=12,

        decimal_places=2

    )

    payment_mode = models.CharField(

        max_length=20,

        choices=PAYMENT_MODE

    )
    
    denomination = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    notes_count = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    custom_denomination = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    transaction_id = models.CharField(
        max_length=150,
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
    # MODEL VALIDATION
    # ==========================================

    def clean(self):

        # Amount Validation

        if self.amount <= 0:

            raise ValidationError({

                "amount":

                "Payment amount must be greater than zero."

            })

        # Maximum Amount

        if self.amount > 999999999:

            raise ValidationError({

                "amount":

                "Payment amount is too large."

            })

        # Payment Date

        if self.payment_date > timezone.now().date():

            raise ValidationError({

                "payment_date":

                "Future payment date is not allowed."

            })
            
            
        # ==========================================
        # Payment Mode Validation
        # ==========================================

        if self.payment_mode == "Cash":

            if not self.denomination:
                raise ValidationError({
                    "denomination": "Please select denomination."
                })

            if not self.notes_count:
                raise ValidationError({
                    "notes_count": "Enter number of notes."
                })

            if self.denomination == "Others" and not self.custom_denomination:
                raise ValidationError({
                    "custom_denomination": "Enter custom denomination."
                })

        elif self.payment_mode in ["UPI", "Bank", "Card"]:

            if not self.transaction_id:
                raise ValidationError({
                    "transaction_id": "Transaction ID is required."
                })

        # Remarks

        if self.remarks:

            self.remarks = self.remarks.strip()

            if len(self.remarks) > 500:

                raise ValidationError({

                    "remarks":

                    "Remarks cannot exceed 500 characters."

                })

    def __str__(self):

        return f"{self.project.project_name} - ₹{self.amount}"
# ==========================================
# PROJECT EXPENSE MODEL
# ==========================================

from django.core.exceptions import ValidationError
from django.utils import timezone
import re


class ProjectExpense(models.Model):
    
    PAYMENT_CHOICES = [
        ("Cash", "Cash"),
        ("UPI", "UPI"),
        ("Bank", "Bank Transfer"),
        ("Card", "Card"),
        ("Cheque", "Cheque"),
    ]

    payment_mode = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
    )
    
    denomination = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    notes_count = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    custom_denomination = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    transaction_id = models.CharField(
        max_length=150,
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

    project = models.ForeignKey(

        Project,

        on_delete=models.CASCADE,

        related_name="expenses"

    )

    expense_name = models.CharField(

        max_length=200

    )

    amount = models.DecimalField(

        max_digits=12,

        decimal_places=2

    )

    expense_date = models.DateField()

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
    # MODEL VALIDATION
    # ==========================================

    def clean(self):

        # Expense Name

        expense = self.expense_name.strip()

        if len(expense) < 3:

            raise ValidationError({

                "expense_name":

                "Expense name must contain at least 3 characters."

            })

        if len(expense) > 100:

            raise ValidationError({

                "expense_name":

                "Expense name cannot exceed 100 characters."

            })

        if not re.match(

            r'^[A-Za-z0-9&().,_\- ]+$',

            expense

        ):

            raise ValidationError({

                "expense_name":

                "Expense name contains invalid characters."

            })

        # Amount

        if self.amount <= 0:

            raise ValidationError({

                "amount":

                "Expense amount must be greater than zero."

            })

        if self.amount > 999999999:

            raise ValidationError({

                "amount":

                "Expense amount is too large."

            })

        # Expense Date

        if self.expense_date > timezone.now().date():

            raise ValidationError({

                "expense_date":

                "Future expense date is not allowed."

            })
            
            
        if self.payment_mode == "Cash":

            if not self.denomination:
                raise ValidationError({
                    "denomination": "Please select denomination."
                })

            if not self.notes_count:
                raise ValidationError({
                    "notes_count": "Enter number of notes."
                })

            if self.denomination == "Others" and not self.custom_denomination:
                raise ValidationError({
                    "custom_denomination": "Enter custom denomination."
                })

        elif self.payment_mode in ["UPI", "Bank", "Card"]:

            if not self.transaction_id:
                raise ValidationError({
                    "transaction_id": "Transaction ID is required."
                })

        elif self.payment_mode == "Cheque":

            if not self.cheque_number:
                raise ValidationError({
                    "cheque_number": "Cheque Number is required."
                })

            if not self.bank_name:
                raise ValidationError({
                    "bank_name": "Bank Name is required."
                })

        # Remarks

        if self.remarks:

            self.remarks = self.remarks.strip()

            if len(self.remarks) > 500:

                raise ValidationError({

                    "remarks":

                    "Remarks cannot exceed 500 characters."

                })

    def __str__(self):

        return self.expense_name
    

# ======================================================
# EMPLOYEE SALARY MODEL
# ======================================================

from django.core.exceptions import ValidationError
from django.utils import timezone
import re


class EmployeeSalary(models.Model):

    PAYMENT_MODE = [

        ("Cash", "Cash"),

        ("UPI", "UPI"),

        ("Bank", "Bank Transfer"),

    ]

    PAYMENT_STATUS = [

        ("Paid", "Paid"),

        ("Pending", "Pending"),

    ]

    employee_name = models.CharField(
        max_length=150
    )

    employee_id = models.CharField(
        max_length=50,
        unique=True
        
    )

    department = models.CharField(
        max_length=100
    )

    designation = models.CharField(
        max_length=100
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE
    )

    salary_month = models.DateField()

    basic_salary = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    bonus = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    deduction = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    net_salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        editable=False
    )

    payment_date = models.DateField()

    payment_mode = models.CharField(
        max_length=20,
        choices=PAYMENT_MODE
    )
    
    # ==========================================
    # CASH DETAILS
    # ==========================================

    DENOMINATION_CHOICES = [

        ("100", "₹100"),
        ("200", "₹200"),
        ("500", "₹500"),
        ("Others", "Others"),

    ]

    denomination = models.CharField(
        max_length=20,
        choices=DENOMINATION_CHOICES,
        blank=True,
        null=True
    )

    notes_count = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    custom_denomination = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    # ==========================================
    # ONLINE PAYMENT
    # ==========================================

    transaction_id = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    # ==========================================
    # CHEQUE
    # ==========================================

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

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default="Pending"
    )

    remarks = models.TextField(
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

    # ==========================================
    # MODEL VALIDATION
    # ==========================================

    def clean(self):

        # Employee Name

        if len(self.employee_name.strip()) < 3:

            raise ValidationError({

                "employee_name":

                "Employee name must contain at least 3 characters."

            })

        if not re.match(

            r'^[A-Za-z ]+$',

            self.employee_name

        ):

            raise ValidationError({

                "employee_name":

                "Employee name must contain only alphabets."

            })

        # Employee ID

        if not self.employee_id:
            raise ValidationError({
                "employee_id": "Employee ID is required."
            })

        self.employee_id = self.employee_id.strip()

        if len(self.employee_id) < 3:
            raise ValidationError({
                "employee_id": "Employee ID must contain at least 3 characters."
            })
            
            
        # ==========================================
        # PAYMENT MODE VALIDATION
        # ==========================================

        if self.payment_mode == "Cash":

            if not self.denomination:
                raise ValidationError({
                    "denomination": "Please select denomination."
                })

            if not self.notes_count:
                raise ValidationError({
                    "notes_count": "Enter number of notes."
                })

            if self.denomination == "Others" and not self.custom_denomination:
                raise ValidationError({
                    "custom_denomination": "Enter custom denomination."
                })

        elif self.payment_mode in ["UPI", "Bank Transfer"]:

            if not self.transaction_id:
                raise ValidationError({
                    "transaction_id": "Transaction ID is required."
                })

                # Department

                if not re.match(

                    r'^[A-Za-z ]+$',

                    self.department

                ):

                    raise ValidationError({

                        "department":

                        "Department must contain only alphabets."

                    })

                # Designation

                if not re.match(

                    r'^[A-Za-z ]+$',

                    self.designation

                ):

                    raise ValidationError({

                        "designation":

                        "Designation must contain only alphabets."

                    })

                # Basic Salary

                if self.basic_salary <= 0:

                    raise ValidationError({

                        "basic_salary":

                        "Basic salary must be greater than zero."

                    })

                # Bonus

                if self.bonus < 0:

                    raise ValidationError({

                        "bonus":

                        "Bonus cannot be negative."

                    })

        # Deduction

        if self.deduction < 0:

            raise ValidationError({

                "deduction":

                "Deduction cannot be negative."

            })

        # Net Salary

        net = self.basic_salary + self.bonus - self.deduction

        if net < 0:

            raise ValidationError({

                "deduction":

                "Deduction cannot exceed total salary."

            })

        # Salary Month

        if self.salary_month and self.salary_month > timezone.localdate():
            raise ValidationError({
                "salary_month": "Future months are not allowed."
            })

        # Payment Date

        if self.payment_date > timezone.now().date():

            raise ValidationError({

                "payment_date":

                "Payment date cannot be a future date."

            })

        # Remarks

        if self.remarks:

            self.remarks = self.remarks.strip()

            if len(self.remarks) > 500:

                raise ValidationError({

                    "remarks":

                    "Remarks cannot exceed 500 characters."

                })

    # ==========================================
    # SAVE
    # ==========================================

    def save(self, *args, **kwargs):

        self.net_salary = (

            self.basic_salary +

            self.bonus -

            self.deduction

        )

        self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self):

        return self.employee_name