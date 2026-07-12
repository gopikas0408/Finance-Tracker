from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

from core.models import BaseModel


# ==========================================================
# MONTHLY TARGET MODEL
# ==========================================================

class MonthlyTarget(BaseModel):

    MONTH_CHOICES = (

        ("January", "January"),
        ("February", "February"),
        ("March", "March"),
        ("April", "April"),
        ("May", "May"),
        ("June", "June"),
        ("July", "July"),
        ("August", "August"),
        ("September", "September"),
        ("October", "October"),
        ("November", "November"),
        ("December", "December"),

    )

    # ======================================================
    # BASIC INFORMATION
    # ======================================================

    month = models.CharField(

        max_length=20,

        choices=MONTH_CHOICES,

    )

    year = models.PositiveIntegerField()

    # ======================================================
    # TARGETS
    # ======================================================

    revenue_target = models.DecimalField(

        max_digits=12,

        decimal_places=2,

    )

    expense_budget = models.DecimalField(

        max_digits=12,

        decimal_places=2,

    )

    profit_target = models.DecimalField(

        max_digits=12,

        decimal_places=2,

    )

    # ======================================================
    # MODEL VALIDATION
    # ======================================================

    def clean(self):

        errors = {}

        current_year = timezone.now().year

        # -------------------------
        # Year
        # -------------------------

        if self.year < current_year:

            errors["year"] = (

                f"Year cannot be less than {current_year}."

            )

        # -------------------------
        # Revenue
        # -------------------------

        if self.revenue_target is None:

            errors["revenue_target"] = (

                "Revenue target is required."

            )

        elif self.revenue_target <= 0:

            errors["revenue_target"] = (

                "Revenue target must be greater than zero."

            )

        # -------------------------
        # Expense Budget
        # -------------------------

        if self.expense_budget is None:

            errors["expense_budget"] = (

                "Expense budget is required."

            )

        elif self.expense_budget < 0:

            errors["expense_budget"] = (

                "Expense budget cannot be negative."

            )

        # -------------------------
        # Profit Target
        # -------------------------

        if self.profit_target is None:

            errors["profit_target"] = (

                "Profit target is required."

            )

        elif self.profit_target < 0:

            errors["profit_target"] = (

                "Profit target cannot be negative."

            )

        # -------------------------
        # Revenue vs Expense
        # -------------------------

        if (

            self.revenue_target is not None

            and self.expense_budget is not None

            and self.revenue_target < self.expense_budget

        ):

            errors["revenue_target"] = (

                "Revenue target must be greater than expense budget."

            )

        # -------------------------
        # Profit Validation
        # -------------------------

        if (

            self.profit_target is not None

            and self.revenue_target is not None

            and self.profit_target > self.revenue_target

        ):

            errors["profit_target"] = (

                "Profit target cannot exceed revenue target."

            )

        if errors:

            raise ValidationError(errors)

    # ======================================================
    # SAVE
    # ======================================================

    def save(self, *args, **kwargs):

        self.full_clean()

        super().save(*args, **kwargs)

    # ======================================================
    # META
    # ======================================================

    class Meta:

        ordering = [

            "-year",

            "-month",

        ]

        unique_together = (

            "month",

            "year",

        )

        indexes = [

            models.Index(

                fields=[

                    "year",

                ]

            ),

            models.Index(

                fields=[

                    "month",

                ]

            ),

        ]

        verbose_name = "Monthly Target"

        verbose_name_plural = "Monthly Targets"

    # ======================================================
    # STRING
    # ======================================================

    def __str__(self):

        return (

            f"{self.month} {self.year}"

        )