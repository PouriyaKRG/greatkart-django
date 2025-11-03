from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin
# Register your models here.


class AccountAdmin(UserAdmin):
    list_display = ('email_address', 'phone_number', 'first_name', 'last_name',
                    'date_joined', 'last_login', 'is_active')

    readonly_fields = ('date_joined', 'last_login')
    ordering = ('-date_joined',)
    list_display_links = ('email_address', 'phone_number')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)
