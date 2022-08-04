"""
    urls
"""

from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


# home
@login_required
def home(request):
	
	"""
		home
	"""
    
	if request.user.user_type == '1':

		response = redirect('adminops/adminops_home')
		return response

	elif request.user.user_type == '2':

		response = redirect('shopuser/shopuser_products')
		return response

	else:
		response = redirect('products/product_list')
		return response


urlpatterns = [
    path('', home, name = "home"),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('account/', include('users.urls')),
    path('products/', include('product.urls')),
    path('shopuser/', include('shopuser.urls')),
    path('adminops/', include('adminops.urls')),
]



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)