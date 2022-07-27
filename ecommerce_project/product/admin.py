from django.contrib import admin
from .models import Category, Brand, Color, Material, Product, ProductAttribute

# admin.site.register(Banner)
admin.site.register(Brand)
admin.site.register(Material)

class CategoryAdmin(admin.ModelAdmin):
	list_display=('title',)
admin.site.register(Category,CategoryAdmin)

class ColorAdmin(admin.ModelAdmin):
	list_display=('title','color_bg')
admin.site.register(Color,ColorAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display=('id','title','category','brand','published',)
    list_editable=('published',)
admin.site.register(Product,ProductAdmin)

# Product Attribute
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display=('id','image_tag','product','price','color','material')
admin.site.register(ProductAttribute,ProductAttributeAdmin)

