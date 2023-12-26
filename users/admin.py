from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('id', 'phone', 'invite_code', 'activated_invite_code')
    ordering = ('phone',)
    fieldsets = (
        (None,
         {'fields': ('phone', 'password', 'is_active',
                     'invite_code', 'activated_invite_code')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
