from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from authentication.models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'company_name')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    add_fieldsets = (
        (None, {
            'fields': ('first_name', 'username', 'email', 'company_name', 'phone', 'password1', 'password2')
        }),
    )

    list_per_page = 25
