from django.urls import path
from . import views



urlpatterns = [
    path("shopuser_signup/", views.signup, name = "account_shopuser_signup"),
    path("shopuser_list/", views.shopuser_list, name = "shopuser_list_approval"),
    path('shopuser_details/<int:user_id>/', views.shopuser_details.as_view(), name = 'shopuser_details'),
    path('shopuser_aproval/', views.shopuser_details.as_view(), name = 'shopuser_aproval'),
    path('shopuser_crud/', views.shopuser_crud, name = 'shopuser_crud'),
    path('shopuser_crud/<int:pk>/update', views.update_shopuser, name='update_shopuser'),
    path('shopuser_delete/<int:pk>/delete', views.delete_shopuser, name='delete_shopuser'),
    path('shopuser_add/', views.shopuser_add, name='add_shopuser'),
    path('<int:pk>/edit_profile/', views.EditProfileCustomer.as_view(), name='edit_profile'),
     path('<int:pk>/edit_profile_shop/', views.EditProfileShopuser.as_view(), name='edit_profile_shop'),
    path('profile/', views.profile, name='profile'),

]