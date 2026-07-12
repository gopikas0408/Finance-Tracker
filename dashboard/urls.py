from . import views
from django.urls import path

urlpatterns = [

    path(
        "",
        views.dashboard,
        name="dashboard"
    ),

    path(
        "search/",
        views.global_search,
        name="global_search"
    ),

]