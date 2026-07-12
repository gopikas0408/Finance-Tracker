from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
import re


class Transaction(models.Model):

    # ==================================================
    # SOURCE MODULE
    # ==================================================

    SOURCE_MODULE = [

        ("Income", "Income"),

        ("Expense", "Expense"),

        ("Services", "IT Services"),

        ("Training", "IT Training"),

    ]

    # ==================================================
    # TRANSACTION TYPE
    # ==================================================

    TRANSACTION_TYPE = [

        ("Income", "Income"),

        ("Expense", "Expense"),

    ]

    # ==================================================
    # PAYMENT MODE
    # ==================================================

    PAYMENT_MODE = [

        ("Cash", "Cash"),

        ("UPI", "UPI"),

        ("Bank", "Bank Transfer"),

        ("Card", "Card"),

        ("Cheque", "Cheque"),

    ]

    # ==================================================
    # STATUS
    # ==================================================

    STATUS = [

        ("Completed", "Completed"),

        ("Pending", "Pending"),
        ("Paid", "Paid"),

        ("Failed", "Failed"),

    ]

    # ==================================================
    # FIELDS
    # ==================================================

    transaction_id = models.CharField(

        max_length=20,

        unique=True,

        editable=False,

    )

    source_module = models.CharField(

        max_length=30,

        choices=SOURCE_MODULE,

    )

    transaction_type = models.CharField(

        max_length=20,

        choices=TRANSACTION_TYPE,

    )

    reference = models.CharField(

        max_length=150,

    )

    # Original Record ID
    # Example:
    # Income.id
    # Expense.id
    # StudentPayment.id
    # EmployeeSalary.id

    reference_id = models.PositiveIntegerField(

        null=True,

        blank=True,

    )

    amount = models.DecimalField(

        max_digits=12,

        decimal_places=2,

    )

    payment_mode = models.CharField(

        max_length=20,

        choices=PAYMENT_MODE,

    )

    transaction_date = models.DateField()

    status = models.CharField(

        max_length=20,

        choices=STATUS,

        default="Completed",

    )

    notes = models.TextField(

        blank=True,

        null=True,

    )

    created_by = models.ForeignKey(

        User,

        on_delete=models.SET_NULL,

        null=True,

        blank=True,

    )

    created_at = models.DateTimeField(

        auto_now_add=True,

    )

    updated_at = models.DateTimeField(

        auto_now=True,

    )

    # ==================================================
    # AUTO TRANSACTION ID
    # ==================================================

    def generate_transaction_id(self):

        last_transaction = Transaction.objects.order_by("-id").first()

        if last_transaction:

            try:

                number = int(

                    last_transaction.transaction_id.replace(

                        "TRX",

                        ""

                    )

                )

            except Exception:

                number = last_transaction.id

            return f"TRX{number + 1:06d}"

        return "TRX000001"
    
        # ==================================================
    # VALIDATION
    # ==================================================

    def clean(self):

        # -------------------------
        # Source Module
        # -------------------------

        if not self.source_module:

            raise ValidationError({

                "source_module":
                "Source module is required."

            })

        # -------------------------
        # Transaction Type
        # -------------------------

        if not self.transaction_type:

            raise ValidationError({

                "transaction_type":
                "Please select transaction type."

            })

        # -------------------------
        # Reference
        # -------------------------

        if not self.reference:

            raise ValidationError({

                "reference":
                "Reference is required."

            })

        self.reference = self.reference.strip()

        if len(self.reference) < 3:

            raise ValidationError({

                "reference":
                "Reference must contain at least 3 characters."

            })

        if len(self.reference) > 150:

            raise ValidationError({

                "reference":
                "Reference is too long."

            })

        # Only allow letters, numbers and common symbols

        if not re.match(

            r"^[A-Za-z0-9\s\-_/().,&]+$",

            self.reference

        ):

            raise ValidationError({

                "reference":
                "Reference contains invalid characters."

            })

        # -------------------------
        # Reference ID
        # -------------------------

        if self.reference_id is not None:

            if self.reference_id <= 0:

                raise ValidationError({

                    "reference_id":
                    "Reference ID must be greater than zero."

                })

        # -------------------------
        # Amount
        # -------------------------

        if self.amount is None:

            raise ValidationError({

                "amount":
                "Amount is required."

            })

        if self.amount <= 0:

            raise ValidationError({

                "amount":
                "Amount must be greater than zero."

            })

        if self.amount > 999999999:

            raise ValidationError({

                "amount":
                "Amount exceeds allowed limit."

            })

        # -------------------------
        # Payment Mode
        # -------------------------

        if not self.payment_mode:

            raise ValidationError({

                "payment_mode":
                "Please select payment mode."

            })

        # -------------------------
        # Transaction Date
        # -------------------------

        if not self.transaction_date:

            raise ValidationError({

                "transaction_date":
                "Transaction date is required."

            })

        if self.transaction_date > timezone.now().date():

            raise ValidationError({

                "transaction_date":
                "Future transaction date is not allowed."

            })

        # -------------------------
        # Status
        # -------------------------

        if not self.status:

            raise ValidationError({

                "status":
                "Please select transaction status."

            })

        if (

            self.status == "Completed"

            and

            self.amount <= 0

        ):

            raise ValidationError({

                "status":
                "Completed transaction must have a valid amount."

            })

        # -------------------------
        # Notes
        # -------------------------

        if self.notes:

            self.notes = self.notes.strip()

            if len(self.notes) < 5:

                raise ValidationError({

                    "notes":
                    "Notes must contain at least 5 characters."

                })

            if len(self.notes) > 500:

                raise ValidationError({

                    "notes":
                    "Notes cannot exceed 500 characters."

                })
                
                
        # ==================================================
    # SAVE
    # ==================================================

    def save(self, *args, **kwargs):

        # Generate Transaction ID
        if not self.transaction_id:

            self.transaction_id = self.generate_transaction_id()

        # Format Reference
        if self.reference:

            self.reference = self.reference.strip().title()

        # Format Notes
        if self.notes:

            self.notes = self.notes.strip()

        # Run Model Validation
        self.full_clean()

        super().save(*args, **kwargs)

    # ==================================================
    # META
    # ==================================================

    class Meta:

        ordering = [

            "-created_at",

        ]

        verbose_name = "Transaction"

        verbose_name_plural = "Transactions"

    # ==================================================
    # STRING REPRESENTATION
    # ==================================================

    def __str__(self):

        return (

            f"{self.transaction_id} | "

            f"{self.source_module} | "

            f"{self.transaction_type} | "

            f"{self.reference} | "

            f"₹{self.amount}"

        )