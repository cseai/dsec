from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField

from .model_utils import PaymentAccountCommonInfo

User = get_user_model()


class BankAccount(PaymentAccountCommonInfo):
    user                = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    bank_name           = models.CharField(max_length=120)
    branch_name         = models.CharField(max_length=120)
    account_type        = models.CharField(max_length=50)
    account_holder_name = models.CharField(max_length=50)
    account_number      = models.CharField(max_length=50)
    routing_number      = models.CharField(max_length=50)


class BkashAccount(PaymentAccountCommonInfo):
    user                = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    account_type        = models.CharField(max_length=50)
    account_holder_name = models.CharField(max_length=50)
    account_number      = PhoneNumberField()

    def __str__(self):
        return f"{self.account_number.as_e164}, {self.account_type}"
