"""
    urls
"""

from django.urls import path
from . import views


urlpatterns = [
    path("product_list/", views.product_list, name = "product_list"),
    path("product_search", views.search, name = "product_search"),
    path("product_list/product_filter", views.filter_data, name = "product_filter"),
    path("product_list/load_more_data", views.load_more_data, name = "load_more_data"),
    path("add_to_cart", views.cart_add, name = "add_to_cart"),
    path("cart_list/", views.cart_list, name = "cart_list"),
    path("delete-from-cart", views.cart_delete, name = "delete_from_cart"),
    path("add_to_wishlist", views.wishlist_add, name = "add_to_wishlist"),
    path("wishlist_list/", views.wishlist_list, name = "wishlist_list"),
    path("delete-from-wishlist", views.wishlist_delete, name = "delete_from_wishlist"),
    path("place_order", views.place_order, name = "place_order"),
    path("buy_now", views.buy_now, name = "buy_now"),
    path("order_list", views.order_list, name = "order_list"),
    path("order_cancel", views.order_cancel, name = "order_cancel"),
    path("product_detail", views.product_detail, name = "product_detail"),


]


