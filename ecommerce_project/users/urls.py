from django.urls import path
from . import views



urlpatterns = [
    path("shopuser_signup/", views.signup, name="account_shopuser_signup"),
]