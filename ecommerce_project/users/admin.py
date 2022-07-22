from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import MyUser



       



class UserAdmin(BaseUserAdmin):
    
    

   
    list_display = ('id', 'email', 'user_type','is_admin', 'is_active')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('user_type',)}),
         ('Permissions', {'fields': ('is_admin',)}),
       
    )
   
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_type', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(MyUser, UserAdmin)

admin.site.unregister(Group)
