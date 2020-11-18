from django.contrib import admin

from .models import (
    BankAccount, 
    BkashAccount,
)

admin.site.register(BankAccount)
admin.site.register(BkashAccount)
