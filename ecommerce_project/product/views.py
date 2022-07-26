import json
from allauth.account import views
from allauth.account import app_settings
from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import HttpResponse

from .models import Product

class ProductView(ListView):
    model = Product
    template_name = "product_list." + app_settings.TEMPLATE_EXTENSION


product_list = ProductView.as_view()
