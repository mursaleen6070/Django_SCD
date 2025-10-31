from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("rooms/", views.rooms_view, name="rooms"),
    path("services/", views.services_view, name="services"),
    path("reviews/", views.reviews_view, name="reviews"),
    path("contact/", views.contact_view, name="contact"),
    path("dashboard/", views.dashboard, name="dashboard"),
]
