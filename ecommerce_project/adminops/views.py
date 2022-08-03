"""
    adminops views
"""

from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required


# home
@login_required
def adminops_home(request):

    """
        home
    """

    customers = get_user_model().objects.filter(user_type = '3')
    shopusers = get_user_model().objects.filter(user_type = '2', is_active = True)

    return render(request, 'adminops_home.html', {'customers':customers, 'shopusers':shopusers})
