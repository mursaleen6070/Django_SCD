from django.urls import path

from . import views

app_name = "bookings"

urlpatterns = [
    path("", views.booking_create, name="booking_form"),
    path("confirm/<str:reference>/", views.booking_confirmation, name="booking_confirmation"),
]
