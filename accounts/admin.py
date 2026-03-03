from django.contrib import admin
from .models import UserProfile, UserAddress


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nickname', 'phone')
    search_fields = ('user__username', 'nickname', 'phone')


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipient_name', 'phone', 'address_line', 'is_default')
    list_filter = ('is_default',)
