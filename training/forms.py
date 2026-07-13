from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
import re
from django.db.models import Sum

from .models import Course, Student, StudentPayment


# =====================================================
# COURSE FORM
# =====================================================

class CourseForm(forms.ModelForm):

    class Meta:

        model = Course

        fields = "__all__"

        widgets = {

            "course_name": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "duration": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "course_fee": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "trainer_name": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "training_mode": forms.Select(attrs={
                "class": "form-select"
            }),

            "status": forms.Select(attrs={
                "class": "form-select"
            }),

            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4
            }),

        }

    # ==========================================
    # COURSE NAME
    # ==========================================

    def clean_course_name(self):

        course_name = self.cleaned_data["course_name"].strip()

        if len(course_name) < 3:

            raise ValidationError(
                "Course name must contain at least 3 characters."
            )

        if not re.match(r"^[A-Za-z0-9 &()-.]+$", course_name):

            raise ValidationError(
                "Course name contains invalid characters."
            )

        qs = Course.objects.filter(
            course_name__iexact=course_name
        )

        if self.instance.pk:

            qs = qs.exclude(
                pk=self.instance.pk
            )

        if qs.exists():

            raise ValidationError(
                "Course name already exists."
            )

        return course_name

    # ==========================================
    # DURATION
    # ==========================================

    def clean_duration(self):

        duration = self.cleaned_data["duration"].strip()

        if len(duration) < 2:

            raise ValidationError(
                "Please enter a valid duration."
            )

        return duration

    # ==========================================
    # COURSE FEE
    # ==========================================

    def clean_course_fee(self):

        fee = self.cleaned_data["course_fee"]

        if fee <= 0:

            raise ValidationError(
                "Course fee must be greater than zero."
            )

        return fee

    # ==========================================
    # TRAINER NAME
    # ==========================================

    def clean_trainer_name(self):

        trainer = self.cleaned_data["trainer_name"].strip()

        if len(trainer) < 3:

            raise ValidationError(
                "Trainer name must contain at least 3 characters."
            )

        if not re.match(r"^[A-Za-z ]+$", trainer):

            raise ValidationError(
                "Trainer name should contain only letters."
            )

        return trainer

    # ==========================================
    # DESCRIPTION
    # ==========================================

    def clean_description(self):

        description = self.cleaned_data.get("description")

        if description and len(description) > 500:

            raise ValidationError(
                "Description cannot exceed 500 characters."
            )

        return description
    
# =====================================================
# STUDENT FORM
# =====================================================

class StudentForm(forms.ModelForm):

    class Meta:

        model = Student

        exclude = (
            "course_fee",
            "trainer_name",
            "status",
            "paid_amount",
            "balance_amount",
            "created_at",
            "updated_at",
        )

        widgets = {

            "student_name": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control"
            }),

            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "maxlength": "10",
                "pattern": "[0-9]{10}",
                "inputmode": "numeric",
            }),

            "gender": forms.Select(attrs={
                "class": "form-select"
            }),

            "date_of_birth": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),

            "address": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3
            }),

            "photo": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),

            "course": forms.Select(attrs={
                "class": "form-select"
            }),
            "course_fee": forms.NumberInput(attrs={
                "class": "form-control",
                "readonly": True
            }),
            "trainer_name": forms.TextInput(attrs={
                "class": "form-control",
                "readonly": True
            }),

            "admission_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),


            "status": forms.Select(attrs={
                "class": "form-select"
            }),

        }

    # ==========================================
    # STUDENT NAME
    # ==========================================

    def clean_student_name(self):

        student_name = self.cleaned_data["student_name"].strip()

        if len(student_name) < 3:

            raise ValidationError(
                "Student name must contain at least 3 characters."
            )

        if not re.match(r"^[A-Za-z ]+$", student_name):

            raise ValidationError(
                "Student name should contain only letters."
            )

        return student_name


    # ==========================================
    # EMAIL
    # ==========================================

    def clean_email(self):

        email = self.cleaned_data["email"].strip().lower()

        email_regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

        if not re.fullmatch(email_regex, email):

            raise ValidationError(
                "Enter a valid email address."
            )

        qs = Student.objects.filter(email=email)

        if self.instance.pk:

            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():

            raise ValidationError(
                "Email already exists."
            )

        return email


    # ==========================================
    # PHONE
    # ==========================================

    def clean_phone(self):

        phone = self.cleaned_data["phone"].strip()

        if not re.fullmatch(r"[6-9]\d{9}", phone):

            raise ValidationError(
                "Phone number must contain exactly 10 digits and start with 6, 7, 8, or 9."
            )

        qs = Student.objects.filter(phone=phone)

        if self.instance.pk:

            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():

            raise ValidationError(
                "Phone number already exists."
            )

        return phone


    # ==========================================
    # DATE OF BIRTH
    # ==========================================

    def clean_date_of_birth(self):

        dob = self.cleaned_data["date_of_birth"]

        today = timezone.localdate()

        if dob > today:

            raise ValidationError(
                "Future date is not allowed."
            )

        age = today.year - dob.year - (
            (today.month, today.day) < (dob.month, dob.day)
        )

        if age < 15:

            raise ValidationError(
                "Student must be at least 15 years old."
            )

        return dob


    # ==========================================
    # ADMISSION DATE
    # ==========================================

    def clean_admission_date(self):

        admission_date = self.cleaned_data.get("admission_date")

        if not admission_date:
            raise ValidationError("Admission Date is required.")

        today = timezone.localdate()

        # Allow today, block only tomorrow and future dates
        if admission_date > today:
            raise ValidationError(
                "Future date is not allowed."
            )

        return admission_date




    # ==========================================
    # ADDRESS
    # ==========================================

    def clean_address(self):

        address = self.cleaned_data.get("address")

        if address and len(address) > 500:

            raise ValidationError(
                "Address cannot exceed 500 characters."
            )

        return address
    
# =====================================================
# STUDENT PAYMENT FORM
# =====================================================

class StudentPaymentForm(forms.ModelForm):
    
    DENOMINATION_CHOICES = [
        ("", "Select"),
        ("100", "₹100"),
        ("200", "₹200"),
        ("500", "₹500"),
        ("Others", "Others"),
    ]

    course_fee = forms.DecimalField(
        required=False,
        disabled=True,
        widget=forms.NumberInput(attrs={
            "class": "form-control"
        })
    )

    paid_amount = forms.DecimalField(
        required=False,
        disabled=True,
        widget=forms.NumberInput(attrs={
            "class": "form-control"
        })
    )

    balance_amount = forms.DecimalField(
        required=False,
        disabled=True,
        widget=forms.NumberInput(attrs={
            "class": "form-control"
        })
    )

    denomination = forms.ChoiceField(
        choices=DENOMINATION_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            "class": "form-select",
            "id": "denomination"
        })
    )

    notes_count = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "id": "notes_count"
        })
    )

    custom_denomination = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "id": "custom_denomination"
        })
    )

    transaction_id = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "id": "transaction_id"
        })
    )

    cheque_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "id": "cheque_number"
        })
    )

    bank_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "id": "bank_name"
        })
    )
        
    
    course_fee = forms.DecimalField(
        required=False,
        disabled=True,
        widget=forms.NumberInput(attrs={
            "class": "form-control"
        })
    )

    paid_amount = forms.DecimalField(
        required=False,
        disabled=True,
        widget=forms.NumberInput(attrs={
            "class": "form-control"
        })
    )

    balance_amount = forms.DecimalField(
        required=False,
        disabled=True,
        widget=forms.NumberInput(attrs={
            "class": "form-control"
        })
    )
    class Meta:

        model = StudentPayment

        fields = "__all__"

        widgets = {

            "student": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "payment_mode": forms.Select(
                attrs={
                    "class": "form-select",
                    "id": "id_payment_mode"
                }
            ),
            

            "payment_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                     "id": "id_payment_date"
                }
            ),

            "remarks": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3
                }
            ),

        }
        def __init__(self, *args, **kwargs):

            super().__init__(*args, **kwargs)

            if self.is_bound:

                student_id = self.data.get("student")

                if student_id:

                    try:

                        student = Student.objects.get(id=student_id)

                        self.fields["course_fee"].initial = student.course_fee

                        self.fields["paid_amount"].initial = student.paid_amount

                        self.fields["balance_amount"].initial = student.balance_amount

                    except Student.DoesNotExist:

                        pass

    # ==========================================
    # STUDENT
    # ==========================================

    def clean_amount(self):

        amount = self.cleaned_data.get("amount")

        student = self.cleaned_data.get("student")

        if amount is None:

            raise ValidationError("Amount is required.")

        if amount <= 0:

            raise ValidationError(
                "Amount must be greater than zero."
            )

        if student:

            if amount > student.balance_amount:

                raise ValidationError(
                    f"Remaining Balance is only ₹{student.balance_amount}."
                )

        return amount

    # ==========================================
    # PAYMENT DATE
    # ==========================================

   

    def clean_payment_date(self):

        payment_date = self.cleaned_data["payment_date"]

        today = timezone.localdate()

        if payment_date > today:
            raise ValidationError(
                "Future Date is not allowed."
            )

        return payment_date

    # ==========================================
    # REMARKS
    # ==========================================

    def clean_remarks(self):

        remarks = self.cleaned_data.get("remarks")

        if remarks and len(remarks) > 500:

            raise ValidationError(
                "Remarks cannot exceed 500 characters."
            )

        return remarks

    # ==========================================
    # COMPLETE FORM VALIDATION
    # ==========================================

  

def clean(self):

    cleaned_data = super().clean()

    payment_mode = cleaned_data.get("payment_mode")

    denomination = cleaned_data.get("denomination")

    notes_count = cleaned_data.get("notes_count")

    custom_denomination = cleaned_data.get("custom_denomination")

    transaction_id = cleaned_data.get("transaction_id")

    cheque_number = cleaned_data.get("cheque_number")

    bank_name = cleaned_data.get("bank_name")

    student = cleaned_data.get("student")

    amount = cleaned_data.get("amount")

    if student and amount:

        total_paid = (
            StudentPayment.objects.filter(student=student)
            .exclude(pk=self.instance.pk)
            .aggregate(total=Sum("amount"))["total"] or 0
        )

        balance = student.course_fee - total_paid

        if amount > balance:

            self.add_error(
                "amount",
                f"Remaining Balance is only ₹{balance}."
            )

    # Cash

    if payment_mode == "Cash":

        if not denomination:

            self.add_error(
                "denomination",
                "Please select denomination."
            )

        if not notes_count:

            self.add_error(
                "notes_count",
                "Enter number of notes."
            )

        if denomination == "Others" and not custom_denomination:

            self.add_error(
                "custom_denomination",
                "Enter custom denomination."
            )

    # UPI / Bank / Card

    elif payment_mode in ["UPI", "Bank", "Card"]:

        if not transaction_id:

            self.add_error(
                "transaction_id",
                "Transaction ID is required."
            )

    # Cheque

    elif payment_mode == "Cheque":

        if not cheque_number:

            self.add_error(
                "cheque_number",
                "Cheque Number is required."
            )

        if not bank_name:

            self.add_error(
                "bank_name",
                "Bank Name is required."
            )

    return cleaned_data