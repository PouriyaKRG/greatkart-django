from django.contrib import admin
from .models import Account, UserProfile
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

class AccountAdmin(UserAdmin):
    list_display = ('email_address', 'phone_number', 'first_name', 'last_name',
                    'date_joined', 'last_login', 'is_active')

    readonly_fields = ('date_joined', 'last_login')
    ordering = ('-date_joined',)
    list_display_links = ('email_address', 'phone_number')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self,object):
        return format_html('<img src="{}" width="50" height="50" style="border-radius:50%" >'.format(object.profile_picture.url))
    thumbnail.short_description = 'Profile Picture'
    list_display = ('thumbnail','user','city','state', 'country')
    list_display_links = ('user',)


admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)