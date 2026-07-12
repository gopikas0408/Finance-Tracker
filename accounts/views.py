from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from .forms import LoginForm

from activity.services import (
    create_notification,
    log_activity,
)


# =====================================================
# LOGIN
# =====================================================

def login_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    form = LoginForm(
        request,
        data=request.POST or None
    )

    if request.method == "POST":

        if form.is_valid():

            user = form.get_user()

            login(
                request,
                user
            )

            create_notification(

                title="User Login",

                message=f"{user.username} logged into the system.",

                module="Accounts",

                action="Login",

                priority="Low",

                user=user,

            )

            log_activity(

                module="Accounts",

                action="Login",

                record_name=user.username,

                description="User logged into the Finance Tracker.",

                user=user,

            )

            return redirect("dashboard")

    return render(

        request,

        "accounts/login.html",

        {

            "form": form,

        }

    )


# =====================================================
# LOGOUT
# =====================================================

@login_required
def logout_view(request):

    create_notification(

        title="User Logout",

        message=f"{request.user.username} logged out from the system.",

        module="Accounts",

        action="Logout",

        priority="Low",

        user=request.user,

    )

    log_activity(

        module="Accounts",

        action="Logout",

        record_name=request.user.username,

        description="User logged out from the Finance Tracker.",

        user=request.user,

    )

    logout(request)

    return redirect("login")