from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone


# =====================================================
# NOTIFICATION MODEL
# =====================================================

class Notification(models.Model):

    MODULE_CHOICES = (
        ("Accounts", "Accounts"),

        ("Income", "Income"),
        ("Expense", "Expense"),
        ("Training", "Training"),
        ("Services", "Services"),
        ("Transaction", "Transaction"),
        ("Report", "Report"),
        ("Settings", "Settings"),
        ("System", "System"),

    )

    ACTION_CHOICES = (

        ("Add", "Add"),
        ("Edit", "Edit"),
        ("Delete", "Delete"),
        ("View", "View"),
        ("Reminder", "Reminder"),
        ("Target", "Target"),
        ("Achievement", "Achievement"),
        ("Login", "Login"),
        ("Logout", "Logout"),

    )

    PRIORITY_CHOICES = (

        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
        ("Critical", "Critical"),

    )

    title = models.CharField(max_length=200)

    message = models.TextField()

    module = models.CharField(
        max_length=30,
        choices=MODULE_CHOICES
    )

    action = models.CharField(
        max_length=30,
        choices=ACTION_CHOICES
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="Medium"
    )

    is_read = models.BooleanField(
        default=False
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = ["-created_at"]

    def clean(self):

        if len(self.title.strip()) < 3:

            raise ValidationError({
                "title": "Notification title must contain at least 3 characters."
            })

        if len(self.message.strip()) < 5:

            raise ValidationError({
                "message": "Notification message is too short."
            })

    def save(self, *args, **kwargs):

        self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self):

        return self.title


# =====================================================
# ACTIVITY LOG MODEL
# =====================================================

class ActivityLog(models.Model):

    module = models.CharField(
        max_length=100
    )

    action = models.CharField(
        max_length=50
    )

    record_name = models.CharField(
        max_length=255
    )

    description = models.TextField()

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = ["-created_at"]

    def clean(self):

        if len(self.module.strip()) < 2:

            raise ValidationError({
                "module": "Module name is required."
            })

        if len(self.action.strip()) < 2:

            raise ValidationError({
                "action": "Action is required."
            })

        if len(self.record_name.strip()) < 2:

            raise ValidationError({
                "record_name": "Record name is required."
            })

    def save(self, *args, **kwargs):

        self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self):

        return f"{self.module} - {self.action}"





# =====================================================
# REMINDER MODEL
# =====================================================

class Reminder(models.Model):

    MODULE_CHOICES = (

        ("Training", "Training"),
        ("Income", "Income"),
        ("Expense", "Expense"),
        ("Services", "Services"),
        ("Transaction", "Transaction"),
        ("General", "General"),

    )

    PRIORITY_CHOICES = (

        ("High", "High"),
        ("Medium", "Medium"),
        ("Low", "Low"),

    )

    STATUS_CHOICES = (

        ("Pending", "Pending"),
        ("Completed", "Completed"),

    )

    title = models.CharField(
        max_length=200
    )

    message = models.TextField()

    module = models.CharField(
        max_length=30,
        choices=MODULE_CHOICES,
        default="General"
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="Medium"
    )

    reminder_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = [
            "reminder_date",
            "-created_at"
        ]

    # ==========================================
    # VALIDATION
    # ==========================================

    def clean(self):

        if len(self.title.strip()) < 3:

            raise ValidationError({
                "title":
                "Reminder title must contain at least 3 characters."
            })

        if len(self.message.strip()) < 5:

            raise ValidationError({
                "message":
                "Reminder message must contain at least 5 characters."
            })

        today = timezone.localdate()

        if self.reminder_date < today:

            raise ValidationError({
                "reminder_date":
                "Past date is not allowed."
            })

    # ==========================================
    # SAVE
    # ==========================================

    def save(self, *args, **kwargs):

        self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self):

        return f"{self.title} - {self.status}"

# =====================================================
# MONTHLY TARGET MODEL
# =====================================================

class MonthlyTarget(models.Model):

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

    month = models.CharField(
        max_length=20,
        choices=MONTH_CHOICES
    )

    year = models.PositiveIntegerField()

    income_target = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    expense_limit = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    profit_target = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = ["-year", "-id"]

        unique_together = (
            "month",
            "year",
        )

    def clean(self):

        current_year = timezone.now().year

        if self.year < current_year:

            raise ValidationError({
                "year": f"Year must be {current_year} or later."
            })

        if self.income_target <= 0:

            raise ValidationError({
                "income_target": "Income target must be greater than zero."
            })

        if self.expense_limit < 0:

            raise ValidationError({
                "expense_limit": "Expense limit cannot be negative."
            })

        if self.profit_target < 0:

            raise ValidationError({
                "profit_target": "Profit target cannot be negative."
            })

        if self.profit_target > self.income_target:

            raise ValidationError({
                "profit_target": "Profit target cannot exceed income target."
            })

        if self.expense_limit > self.income_target:

            raise ValidationError({
                "expense_limit": "Expense limit cannot exceed income target."
            })

    def save(self, *args, **kwargs):

        self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self):

        return f"{self.month} {self.year}"
    
# =====================================================
# ACHIEVEMENT MODEL
# =====================================================

class Achievement(models.Model):

    STATUS_CHOICES = (
        ("Achieved", "Achieved"),
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField()

    achieved_date = models.DateField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Achieved"
    )

    class Meta:

        ordering = ["-achieved_date", "-id"]

    def __str__(self):

        return self.title