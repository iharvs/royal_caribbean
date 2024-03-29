from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("populate_timezones", views.populate_timezones, name="populate_timezones"),
    path("populate_zone_details", views.populate_zone_details, name="populate_zone_details"),
]