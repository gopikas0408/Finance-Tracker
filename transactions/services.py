from django.utils import timezone

from .models import Transaction

from activity.models import Notification, ActivityLog


class TransactionService:

    # =====================================================
    # CREATE TRANSACTION
    # =====================================================

    @staticmethod
    def create_transaction(
        *,
        source_module,
        transaction_type,
        reference,
        amount,
        payment_mode,
        status="Completed",
        notes="",
        user=None,
    ):

        transaction = Transaction.objects.create(

            source_module=source_module,

            transaction_type=transaction_type,

            reference=reference,

            amount=amount,

            payment_mode=payment_mode,

            transaction_date=timezone.now().date(),

            status=status,

            notes=notes or "",

            created_by=user,

        )

        Notification.objects.create(

            title=f"{transaction_type} Added",

            message=f"{reference} (₹{amount}) added successfully.",

            module=source_module,

            action="Add",

            priority="Medium",

            created_by=user,

        )

        ActivityLog.objects.create(

            module=source_module,

            action="Add",

            record_name=reference,

            description=f"{transaction_type} transaction {transaction.transaction_id} created.",

            user=user,

        )

        return transaction

    # =====================================================
    # UPDATE TRANSACTION
    # =====================================================

    @staticmethod
    def update_transaction(
        *,
        source_module,
        reference,
        amount,
        payment_mode,
        status="Completed",
        notes="",
        user=None,
    ):

        transaction = Transaction.objects.filter(

            source_module=source_module,

            reference=reference,

        ).first()

        if not transaction:

            return None

        transaction.amount = amount

        transaction.payment_mode = payment_mode

        transaction.status = status

        transaction.notes = notes or ""

        transaction.transaction_date = timezone.now().date()

        transaction.save()

        Notification.objects.create(

            title="Transaction Updated",

            message=f"{transaction.transaction_id} updated successfully.",

            module=source_module,

            action="Edit",

            priority="Low",

            created_by=user,

        )

        ActivityLog.objects.create(

            module=source_module,

            action="Edit",

            record_name=reference,

            description=f"{transaction.transaction_id} updated.",

            user=user,

        )

        return transaction

    # =====================================================
    # DELETE TRANSACTION
    # =====================================================

    @staticmethod
    def delete_transaction(
        *,
        source_module,
        reference,
        user=None,
    ):

        transaction = Transaction.objects.filter(

            source_module=source_module,

            reference=reference,

        ).first()

        if not transaction:

            return

        transaction_id = transaction.transaction_id

        transaction.delete()

        Notification.objects.create(

            title="Transaction Deleted",

            message=f"{transaction_id} deleted successfully.",

            module=source_module,

            action="Delete",

            priority="High",

            created_by=user,

        )

        ActivityLog.objects.create(

            module=source_module,

            action="Delete",

            record_name=reference,

            description=f"{transaction_id} deleted.",

            user=user,

        )