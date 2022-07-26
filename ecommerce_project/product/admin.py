from django.contrib import admin
from .models import *

# Register your models here.

#category
class CategoryAdmin(admin.ModelAdmin):
	list_display=('name',)

admin.site.register(Category,CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
	list_display=('id','name','category','brand','published','rating')

admin.site.register(Product,ProductAdmin)