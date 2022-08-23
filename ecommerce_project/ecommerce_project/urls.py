"""
    urls
"""

from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from .views import Home


urlpatterns = [
    path('', Home.as_view(), name = "home"),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('account/', include('users.urls')),
    path('products/', include('product.urls')),
    path('shopuser/', include('shopuser.urls')),
    path('adminops/', include('adminops.urls')),
]



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)