from django.contrib import admin

from user.models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'avatar', ]
