from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import re
from .models import (
    Client,
    Project,
    ProjectPayment,
    ProjectPaymentCashDenomination,
    ProjectExpense,
    ProjectExpenseCashDenomination,
    EmployeeSalary,
    EmployeeSalaryCashDenomination,
)
from django.forms import inlineformset_factory

# ======================================================
# CLIENT FORM
# ======================================================

class ClientForm(forms.ModelForm):

    phone = forms.CharField(

        validators=[

            RegexValidator(

                regex=r'^[6-9]\d{9}$',

                message="Phone number must contain exactly 10 digits."

            )

        ]

    )

    class Meta:

        model = Client

        fields = "__all__"

        widgets = {

            "company_name": forms.TextInput(

                attrs={

                    "class":"form-control",

                    "placeholder":"Enter Company Name"

                }

            ),

            "contact_person": forms.TextInput(

                attrs={

                    "class":"form-control",

                    "placeholder":"Enter Contact Person"

                }

            ),

            "phone": forms.TextInput(

                attrs={

                    "class":"form-control",

                    "maxlength":"10",

                    "placeholder":"9876543210"

                }

            ),

            "email": forms.EmailInput(

                attrs={

                    "class":"form-control",

                    "placeholder":"company@gmail.com"

                }

            ),

            "address": forms.Textarea(

                attrs={

                    "class":"form-control",

                    "rows":3,

                    "placeholder":"Enter Address"

                }

            ),

            "gst_number": forms.TextInput(

                attrs={

                    "class":"form-control",

                    "placeholder":"29ABCDE1234F1Z5"

                }

            ),

            "status": forms.Select(

                attrs={

                    "class":"form-select"

                }

            ),

        }

    # ======================================
    # COMPANY NAME
    # ======================================

    def clean_company_name(self):

        company = self.cleaned_data["company_name"].strip()

        if len(company) < 3:

            raise ValidationError(

                "Company name must contain at least 3 characters."

            )

        if not re.match(

            r'^[A-Za-z0-9&.,()\- ]+$',

            company

        ):

            raise ValidationError(

                "Company name contains invalid characters."

            )

        return company

    # ======================================
    # CONTACT PERSON
    # ======================================

    def clean_contact_person(self):

        person = self.cleaned_data["contact_person"].strip()

        if not re.match(

            r'^[A-Za-z ]+$',

            person

        ):

            raise ValidationError(

                "Contact person must contain only letters."

            )

        return person.title()

    # ======================================
    # PHONE
    # ======================================

    def clean_phone(self):

        phone = self.cleaned_data["phone"]

        qs = Client.objects.filter(

            phone=phone

        )

        if self.instance.pk:

            qs = qs.exclude(

                pk=self.instance.pk

            )

        if qs.exists():

            raise ValidationError(

                "Phone number already exists."

            )

        return phone

    # ======================================
    # EMAIL
    # ======================================

    def clean_email(self):

        email = self.cleaned_data["email"].lower()

        qs = Client.objects.filter(

            email=email

        )

        if self.instance.pk:

            qs = qs.exclude(

                pk=self.instance.pk

            )

        if qs.exists():

            raise ValidationError(

                "Email already exists."

            )

        return email

    # ======================================
    # GST
    # ======================================

    def clean_gst_number(self):

        gst = self.cleaned_data.get("gst_number")

        if gst:

            gst = gst.upper()

            pattern = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][1-9A-Z]Z[0-9A-Z]$'

            if not re.match(pattern, gst):

                raise ValidationError(

                    "Enter a valid GST Number."

                )

        return gst


# ======================================================
# PROJECT FORM
# ======================================================

class ProjectForm(forms.ModelForm):

    class Meta:

        model = Project

        fields = "__all__"

        widgets = {

            "client": forms.Select(attrs={
                "class": "form-select"
            }),

            "project_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Project Name"
            }),

            "service_type": forms.Select(attrs={
                "class": "form-select"
            }),

            "project_amount": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Project Amount"
            }),

            "start_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),

            "end_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),

            "status": forms.Select(attrs={
                "class": "form-select"
            }),

            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Project Description"
            }),

        }

    # ==========================================
    # PROJECT NAME
    # ==========================================

    def clean_project_name(self):

        project = self.cleaned_data["project_name"].strip()

        if len(project) < 3:

            raise ValidationError(
                "Project name must contain at least 3 characters."
            )

        if len(project) > 100:

            raise ValidationError(
                "Project name cannot exceed 100 characters."
            )

        if not re.match(

            r'^[A-Za-z0-9&().,_\- ]+$',

            project

        ):

            raise ValidationError(

                "Project name contains invalid characters."

            )

        return project.title()

    # ==========================================
    # PROJECT AMOUNT
    # ==========================================

    def clean_project_amount(self):

        amount = self.cleaned_data["project_amount"]

        if amount <= 0:

            raise ValidationError(

                "Project amount must be greater than zero."

            )

        if amount > 999999999:

            raise ValidationError(

                "Project amount is too large."

            )

        return amount

    # ==========================================
    # START DATE
    # ==========================================

    def clean_start_date(self):

        start = self.cleaned_data["start_date"]

        from datetime import date

        if start > date.today():

            raise ValidationError(

                "Start date cannot be a future date."

            )

        return start

    # ==========================================
    # END DATE
    # ==========================================

    def clean(self):

        cleaned_data = super().clean()

        start = cleaned_data.get("start_date")

        end = cleaned_data.get("end_date")

        if start and end:

            if end < start:

                self.add_error(

                    "end_date",

                    "End date cannot be before Start Date."

                )

        return cleaned_data

    # ==========================================
    # DESCRIPTION
    # ==========================================

    def clean_description(self):

        description = self.cleaned_data.get("description")

        if description:

            description = description.strip()

            if len(description) > 500:

                raise ValidationError(

                    "Description cannot exceed 500 characters."

                )

        return description
    

        
# ======================================================
# PROJECT PAYMENT FORM
# ======================================================

class ProjectPaymentForm(forms.ModelForm):
    
    

    

    transaction_id = forms.CharField(

        required=False,

        widget=forms.TextInput(

            attrs={

                "class": "form-control",

                "id": "transaction_id"

            }

        )

    )

    cheque_number = forms.CharField(

        required=False,

        widget=forms.TextInput(

            attrs={

                "class": "form-control",

                "id": "cheque_number"

            }

        )

    )

    bank_name = forms.CharField(

        required=False,

        widget=forms.TextInput(

            attrs={

                "class": "form-control",

                "id": "bank_name"

            }

        )

    )

    class Meta:
        

        model = ProjectPayment

        fields = [

            "project",

            "payment_mode",

            "amount",

            "payment_date",

            "remarks",

            "transaction_id",

            "cheque_number",

            "bank_name",

        ]

        widgets = {

            "project": forms.Select(attrs={
                "class": "form-select"
            }),

            "amount": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Payment Amount"
            }),

            "payment_mode": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "payment_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),

            "remarks": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Enter Remarks (Optional)"
            }),
            "attachment": forms.ClearableFileInput(
                attrs={
                    "class": "form-control"
                }
            ),

        }
    
    def __init__(self, *args, **kwargs):
    
        super().__init__(*args, **kwargs)
    
        if self.instance and self.instance.pk:
    
            self.fields["denomination"].disabled = True
            self.fields["notes_count"].disabled = True
            self.fields["amount"].disabled = True
        
            

    # ==========================================
    # PROJECT
    # ==========================================

    def clean_project(self):

        project = self.cleaned_data.get("project")

        if not project:

            raise ValidationError(

                "Please select a project."

            )

        return project

    # ==========================================
    # AMOUNT
    # ==========================================

    def clean_amount(self):

        amount = self.cleaned_data["amount"]

        if amount <= 0:

            raise ValidationError(

                "Amount must be greater than zero."

            )

        if amount > 999999999:

            raise ValidationError(

                "Amount is too large."

            )

        return amount

    # ==========================================
    # PAYMENT DATE
    # ==========================================

    def clean_payment_date(self):

        payment_date = self.cleaned_data["payment_date"]

        from datetime import date

        if payment_date > date.today():

            raise ValidationError(

                "Payment date cannot be a future date."

            )

        return payment_date
    
    
    def clean(self):

        cleaned_data = super().clean()

        payment_mode = cleaned_data.get("payment_mode")
        transaction = cleaned_data.get("transaction_id")
        cheque = cleaned_data.get("cheque_number")
        bank = cleaned_data.get("bank_name")

        if payment_mode in ["UPI", "Bank", "Card"]:

            if not transaction:
                self.add_error(
                    "transaction_id",
                    "Transaction ID is required."
                )

        elif payment_mode == "Cheque":

            if not cheque:
                self.add_error(
                    "cheque_number",
                    "Cheque Number is required."
                )

            if not bank:
                self.add_error(
                    "bank_name",
                    "Bank Name is required."
                )

        return cleaned_data

    # ==========================================
    # REMARKS
    # ==========================================

    def clean_remarks(self):

        remarks = self.cleaned_data.get("remarks")

        if remarks:

            remarks = remarks.strip()

            if len(remarks) > 500:

                raise ValidationError(

                    "Remarks cannot exceed 500 characters."

                )

        return remarks
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:

            self.fields["project"].disabled = True
            self.fields["payment_mode"].disabled = True
            self.fields["amount"].disabled = True
            self.fields["payment_date"].disabled = True
            self.fields["transaction_id"].disabled = True
            self.fields["cheque_number"].disabled = True
            self.fields["bank_name"].disabled = True
    
class ProjectPaymentCashDenominationForm(forms.ModelForm):

    class Meta:
        model = ProjectPaymentCashDenomination
        fields = [
            "denomination",
            "notes_count",
            "amount",
        ]

        widgets = {
            "denomination": forms.Select(attrs={"class": "form-select"}),
            "notes_count": forms.NumberInput(attrs={"class": "form-control"}),
            "amount": forms.NumberInput(attrs={
                "class": "form-control",
                "readonly": True
            }),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:

            self.fields["denomination"].disabled = True
            self.fields["notes_count"].disabled = True
            self.fields["amount"].disabled = True
ProjectPaymentCashDenominationFormSet = inlineformset_factory(
    ProjectPayment,
    ProjectPaymentCashDenomination,
    form=ProjectPaymentCashDenominationForm,
    extra=1,
    can_delete=True,
)

ProjectPaymentCashDenominationEditFormSet = inlineformset_factory(
    ProjectPayment,
    ProjectPaymentCashDenomination,
    form=ProjectPaymentCashDenominationForm,
    extra=0,
    can_delete=False
)
# ======================================================
# PROJECT EXPENSE FORM
# ======================================================

class ProjectExpenseForm(forms.ModelForm):

   

    transaction_id = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "id": "transaction_id",
            "placeholder": "Enter Transaction ID"
        })
    )

    cheque_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "id": "cheque_number",
            "placeholder": "Enter Cheque Number"
        })
    )

    bank_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "id": "bank_name",
            "placeholder": "Enter Bank Name"
        })
    )

    class Meta:

        model = ProjectExpense

        fields = [
            "project",
            "expense_name",
            "amount",
            "payment_mode",
            "expense_date",
            "remarks",
            "transaction_id",
            "cheque_number",
            "bank_name",
        ]

        widgets = {

            "project": forms.Select(attrs={
                "class": "form-select"
            }),

            "expense_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Expense Name"
            }),

            "amount": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Expense Amount"
            }),

            "payment_mode": forms.Select(attrs={
                "class": "form-select"
            }),

            "expense_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),

            "remarks": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Enter Remarks (Optional)"
            }),

        }
    
    def __init__(self, *args, **kwargs):
    
            super().__init__(*args, **kwargs)
    
            if self.instance and self.instance.pk:
    
                self.fields["project"].disabled = True
                self.fields["expense_name"].disabled = True
                self.fields["amount"].disabled = True
                self.fields["payment_mode"].disabled = True
                self.fields["expense_date"].disabled = True
                self.fields["transaction_id"].disabled = True
                self.fields["cheque_number"].disabled = True
                self.fields["bank_name"].disabled = True
    # ==========================================
    # PROJECT
    # ==========================================

    def clean_project(self):

        project = self.cleaned_data.get("project")

        if not project:

            raise ValidationError(

                "Please select a project."

            )

        return project

    # ==========================================
    # EXPENSE NAME
    # ==========================================

    def clean_expense_name(self):

        expense = self.cleaned_data["expense_name"].strip()

        if len(expense) < 3:

            raise ValidationError(

                "Expense name must contain at least 3 characters."

            )

        if len(expense) > 100:

            raise ValidationError(

                "Expense name cannot exceed 100 characters."

            )

        if not re.match(

            r'^[A-Za-z0-9&().,_\- ]+$',

            expense

        ):

            raise ValidationError(

                "Expense name contains invalid characters."

            )

        return expense.title()

    # ==========================================
    # AMOUNT
    # ==========================================

    def clean_amount(self):

        amount = self.cleaned_data["amount"]

        if amount <= 0:

            raise ValidationError(

                "Expense amount must be greater than zero."

            )

        if amount > 999999999:

            raise ValidationError(

                "Expense amount is too large."

            )

        return amount

    # ==========================================
    # EXPENSE DATE
    # ==========================================

    def clean_expense_date(self):

        expense_date = self.cleaned_data["expense_date"]

        from datetime import date

        if expense_date > date.today():

            raise ValidationError(

                "Expense date cannot be a future date."

            )

        return expense_date
    
    
    def clean(self):

        cleaned_data = super().clean()

        payment_mode = cleaned_data.get("payment_mode")
        transaction_id = cleaned_data.get("transaction_id")
        cheque_number = cleaned_data.get("cheque_number")
        bank_name = cleaned_data.get("bank_name")

        if payment_mode in ["UPI", "Bank", "Card"]:

            if not transaction_id:
                self.add_error(
                    "transaction_id",
                    "Transaction ID is required."
                )

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

    # ==========================================
    # REMARKS
    # ==========================================

    def clean_remarks(self):

        remarks = self.cleaned_data.get("remarks")

        if remarks:

            remarks = remarks.strip()

            if len(remarks) > 500:

                raise ValidationError(

                    "Remarks cannot exceed 500 characters."

                )

        return remarks
# ======================================================
# PROJECT EXPENSE CASH DENOMINATION FORM
# ======================================================

class ProjectExpenseCashDenominationForm(forms.ModelForm):

    class Meta:

        model = ProjectExpenseCashDenomination

        fields = [
            "denomination",
            "notes_count",
            "amount",
        ]

        widgets = {

            "denomination": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "notes_count": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1
                }
            ),

            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "readonly": True
                }
            ),

        }
        
ProjectExpenseCashDenominationFormSet = inlineformset_factory(
    ProjectExpense,
    ProjectExpenseCashDenomination,
    form=ProjectExpenseCashDenominationForm,
    extra=1,
    can_delete=True,
)

ProjectExpenseCashDenominationEditFormSet = inlineformset_factory(
    ProjectExpense,
    ProjectExpenseCashDenomination,
    form=ProjectExpenseCashDenominationForm,
    extra=0,
    can_delete=False,
)
# ======================================================
# EMPLOYEE SALARY FORM
# ======================================================

class EmployeeSalaryForm(forms.ModelForm):
    
   

    transaction_id = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "transaction_id",
                "placeholder": "Enter Transaction ID",
            }
        ),
    )

    cheque_number = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "cheque_number",
                "placeholder": "Enter Cheque Number",
            }
        ),
    )

    bank_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "bank_name",
                "placeholder": "Enter Bank Name",
            }
        ),
    )

    class Meta:

        model = EmployeeSalary

        fields = [
            "employee_name",
            "employee_id",
            "department",
            "designation",
            "project",
            "salary_month",
            "basic_salary",
            "bonus",
            "deduction",
            "net_salary",
            "payment_date",
            "payment_mode",
            "payment_status",
            "remarks",
            "transaction_id",
            "cheque_number",
            "bank_name",
        ]

        widgets = {

            "employee_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Employee Name"
            }),

            "employee_id": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "EMP001"
            }),

            "department": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Department"
            }),

            "designation": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Designation"
            }),

            "project": forms.Select(attrs={
                "class": "form-select"
            }),

            "salary_month": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),

            "basic_salary": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Basic Salary"
            }),

            "bonus": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Bonus"
            }),

            "deduction": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Deduction"
            }),
            "net_salary": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "readonly": True,
                }
            ),

            "payment_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),

            "payment_mode": forms.Select(attrs={
                "class": "form-select"
            }),

            "payment_status": forms.Select(attrs={
                "class": "form-select"
            }),

            "remarks": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Enter Remarks"
            }),

        }
    
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:

            readonly_fields = [
                
                "salary_month",
                "payment_mode",
                "basic_salary",
                "bonus",
                "deduction",
                "net_salary",
                "payment_date",
                "payment_status",
                "transaction_id",
                "cheque_number",
                "bank_name",
            ]

            for field in readonly_fields:

                if field in self.fields:

                    self.fields[field].disabled = True

    # =====================================
    # EMPLOYEE NAME
    # =====================================

    def clean_employee_name(self):

        employee = self.cleaned_data["employee_name"].strip()

        if len(employee) < 3:

            raise ValidationError(
                "Employee name must contain at least 3 characters."
            )

        if not re.match(r'^[A-Za-z ]+$', employee):

            raise ValidationError(
                "Employee name must contain only alphabets."
            )

        return employee.title()

    # =====================================
    # EMPLOYEE ID
    # =====================================

    def clean_employee_id(self):

        employee_id = self.cleaned_data["employee_id"].upper().strip()

        qs = EmployeeSalary.objects.filter(
            employee_id=employee_id
        )

        if self.instance.pk:

            qs = qs.exclude(
                pk=self.instance.pk
            )

        if qs.exists():

            raise ValidationError(
                "Employee ID already exists."
            )

        return employee_id

    # =====================================
    # DEPARTMENT
    # =====================================

    def clean_department(self):

        department = self.cleaned_data["department"].strip()

        if not re.match(r'^[A-Za-z ]+$', department):

            raise ValidationError(
                "Department must contain only alphabets."
            )

        return department.title()

    # =====================================
    # DESIGNATION
    # =====================================

    def clean_designation(self):

        designation = self.cleaned_data["designation"].strip()

        if not re.match(r'^[A-Za-z ]+$', designation):

            raise ValidationError(
                "Designation must contain only alphabets."
            )

        return designation.title()

    # =====================================
    # BASIC SALARY
    # =====================================

    def clean_basic_salary(self):

        salary = self.cleaned_data["basic_salary"]

        if salary <= 0:

            raise ValidationError(
                "Basic salary must be greater than zero."
            )

        return salary

    # =====================================
    # BONUS
    # =====================================

    def clean_bonus(self):

        bonus = self.cleaned_data.get("bonus") or 0

        if bonus < 0:

            raise ValidationError(
                "Bonus cannot be negative."
            )

        return bonus

    # =====================================
    # DEDUCTION
    # =====================================

    def clean_deduction(self):

        deduction = self.cleaned_data.get("deduction") or 0

        if deduction < 0:

            raise ValidationError(
                "Deduction cannot be negative."
            )

        return deduction

    # =====================================
    # PAYMENT DATE
    # =====================================

    def clean_payment_date(self):

        payment_date = self.cleaned_data["payment_date"]

        from datetime import date

        if payment_date > date.today():

            raise ValidationError(
                "Payment date cannot be a future date."
            )

        return payment_date
    
    # =====================================
    # PAYMENT MODE VALIDATION
    # =====================================

    def clean(self):

        cleaned_data = super().clean()

        payment_mode = cleaned_data.get("payment_mode")
        transaction_id = cleaned_data.get("transaction_id")
        cheque_number = cleaned_data.get("cheque_number")
        bank_name = cleaned_data.get("bank_name")

        if payment_mode in ["UPI", "Bank Transfer"]:

            if not transaction_id:
                self.add_error(
                    "transaction_id",
                    "Transaction ID is required."
                )

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

    # =====================================
    # REMARKS
    # =====================================

    def clean_remarks(self):

        remarks = self.cleaned_data.get("remarks")

        if remarks:

            remarks = remarks.strip()

            if len(remarks) > 500:

                raise ValidationError(
                    "Remarks cannot exceed 500 characters."
                )

        return remarks
    
    
class EmployeeSalaryCashDenominationForm(forms.ModelForm):

    class Meta:

        model = EmployeeSalaryCashDenomination

        fields = [
            "denomination",
            "notes_count",
            "amount",
        ]

        widgets = {

            "denomination": forms.Select(
                attrs={
                    "class": "form-select denomination"
                }
            ),

            "notes_count": forms.NumberInput(
                attrs={
                    "class": "form-control notes",
                    "min": 1,
                }
            ),

            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control amount",
                    "readonly": True,
                }
            ),

        }
        
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:

            self.fields["denomination"].disabled = True
            self.fields["notes_count"].disabled = True
            self.fields["amount"].disabled = True
            
EmployeeSalaryCashDenominationFormSet = inlineformset_factory(
    EmployeeSalary,
    EmployeeSalaryCashDenomination,
    form=EmployeeSalaryCashDenominationForm,
    extra=1,
    can_delete=True,
)

EmployeeSalaryCashDenominationEditFormSet = inlineformset_factory(
    EmployeeSalary,
    EmployeeSalaryCashDenomination,
    form=EmployeeSalaryCashDenominationForm,
    extra=0,
    can_delete=False,
)