"""
    urls
"""

from django.urls import path
from . import views


urlpatterns = [
    
    path("shopuser_products/", views.shopuser_products, name = "shopuser_products"),
    path("publish_unpublish/", views.pblish_unpblish_products, name = "publish_unpublish"),
    path("product_update/", views.product_update, name = "product_update"),
    path("product_delete/", views.product_delete, name = "product_delete"),
    path("product_add/", views.product_add, name = "product_add"),
    path("shopuser_order_list/", views.shopuser_order_list, name = "shopuser_order_list"),


]

