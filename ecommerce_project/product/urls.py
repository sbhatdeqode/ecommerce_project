from django.urls import path
from . import views


urlpatterns = [
    path("product_list/", views.product_list, name = "product_list"),
    path("product_search", views.search, name = "product_search"),
     path("product_list/product_filter", views.filter_data, name = "product_filter"),

]


