from django.urls import path

from . import views

app_name = "drifters"

urlpatterns = [
    path("", views.index, name="index"),
    path("motd", views.motd, name="motd"),
]
