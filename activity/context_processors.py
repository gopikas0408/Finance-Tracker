from .models import Notification

def notification_context(request):

    unread_notifications = Notification.objects.filter(
        is_read=False
    ).count()

    recent_notifications = Notification.objects.filter(
        is_read=False
    ).order_by("-created_at")[:5]

    return {
        "unread_notifications": unread_notifications,
        "recent_notifications": recent_notifications,
    }