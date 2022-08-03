"""
    urls
"""

from django.urls import path
from . import views


urlpatterns = [
    path("adminops_home/", views.adminops_home, name = "adminops_home"),
    
]


