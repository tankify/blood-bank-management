from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("donors/", views.donors, name="donors"),
    path("donors/register/", views.register_donor, name="register_donor"),
    path("requests/", views.requests, name="requests"),
    path("requests/new/", views.create_request, name="create_request"),
    path("banks/", views.banks, name="banks"),
    path("camps/", views.camps, name="camps"),
    path("map/", views.map_search, name="map_search"),
    path("account/register/", views.register, name="register"),
    path("account/login/", auth_views.LoginView.as_view(template_name="portal/login.html"), name="login"),
    path("account/logout/", views.logout_view, name="logout"),
]
