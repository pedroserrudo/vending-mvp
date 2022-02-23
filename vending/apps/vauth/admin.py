from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _

from .models import VendingUser


class VendingUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'deposit', 'role', 'is_staff')
    fieldsets = (
            (None, {'fields': ('username', 'password')}),
            (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
            (_('Vending Role'), {'fields': ('role', )}),
            (_('Permissions'), {
                'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            }),
            (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        )
    readonly_fields = ('deposit', )


admin.site.register(VendingUser, VendingUserAdmin)
