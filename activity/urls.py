from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.notification_center,
        name="activity_center",
    ),

    path(
        "notifications/",
        views.notification_list,
        name="notification_list",
    ),

    path(
        "history/",
        views.activity_history,
        name="activity_history",
    ),

    path(
        "reminders/",
        views.reminder_list,
        name="reminder_list",
    ),

    path(
        "targets/",
        views.target_list,
        name="target_list",
    ),

    path(
        "achievements/",
        views.achievement_list,
        name="achievement_list",
    ),
    
    

]