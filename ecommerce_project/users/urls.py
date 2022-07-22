from django.urls import path
from . import views



urlpatterns = [
    path("shopuser_signup/", views.signup, name = "account_shopuser_signup"),
    path("shopuser_list/", views.shopuser_list, name = "shopuser_list_approval"),
    path('shopuser_details/<int:user_id>/', views.shopuser_details.as_view(), name = 'shopuser_details'),
    path('shopuser_aproval/', views.shopuser_details.as_view(), name = 'shopuser_aproval'),
]