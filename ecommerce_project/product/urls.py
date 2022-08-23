"""
    urls
"""

from django.urls import path
from . import views


urlpatterns = [
    
    path("product_list/", views.ProductList.as_view(), name = "product_list"),
    path("product_search", views.Search.as_view(), name = "product_search"),
    path("product_list/product_filter", views.FilterData.as_view(), name = "product_filter"),
    path("add_to_cart", views.CartAdd.as_view(), name = "add_to_cart"),
    path("cart_list/", views.CartList.as_view(), name = "cart_list"),
    path("delete-from-cart", views.CartDelete.as_view(), name = "delete_from_cart"),
    path("add_to_wishlist", views.WishlistAdd.as_view(), name = "add_to_wishlist"),
    path("wishlist_list/", views.WishlistList.as_view(), name = "wishlist_list"),
    path("delete-from-wishlist", views.WishlistDelete.as_view(), name = "delete_from_wishlist"),
    path("place_order", views.PlaceOrder.as_view(), name = "place_order"),
    path("buy_now", views.BuyNow.as_view(), name = "buy_now"),
    path("order_list", views.OrderList.as_view(), name = "order_list"),
    path("order_cancel", views.OrderCancel.as_view(), name = "order_cancel"),
    path("product_detail", views.ProductDetail.as_view(), name = "product_detail"),

]


