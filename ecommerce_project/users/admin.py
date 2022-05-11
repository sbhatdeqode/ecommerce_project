from tabnanny import verbose
from django.contrib import admin

from django.contrib.auth.models import User
from .models import Users 
from django.contrib.auth.admin import UserAdmin

class UsersInline(admin.StackedInline):
    model = Users
    can_delete=False
    verbose_name_plural='Users'

class CustomisedUserAdmin(UserAdmin):
     inlines = [UsersInline]

admin.site.unregister(User)
admin.site.register(User,CustomisedUserAdmin)


