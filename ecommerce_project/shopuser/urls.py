"""
    urls
"""

from django.urls import path
from . import views


urlpatterns = [
    
    path("shopuser_products/", views.ShopuserProducts.as_view(), name = "shopuser_products"),
    path("publish_unpublish/", views.PblishUnpblish.as_view(), name = "publish_unpublish"),
    path("product_update/", views.ProductUupdate.as_view(), name = "product_update"),
    path("product_delete/", views.ProductDelete.as_view(), name = "product_delete"),
    path("product_add/", views.ProductAdd.as_view(), name = "product_add"),
    path("shopuser_order_list/", views.ShopuserOrderList.as_view(), name = "shopuser_order_list"),
     path("shopuser_order_percentage/", views.ShopuserOrderPercentage.as_view(), name = "shopuser_order_percentage"),


]

