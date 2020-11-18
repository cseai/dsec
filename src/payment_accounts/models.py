from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField

from .model_utils import PaymentAccountCommonInfo

User = get_user_model()

################### NOTE FOR ACCOUNT ########################
# All ACCOUNT (ONLY those are related to ACCOUNT) 
# must end with 'Account' for the custom queryset of GFK relationship
# i.e: 'BankAccount', 'BkashAccount' are VALID for ACCOUNT
# and 'AccountBkash' , 'Bkash', 'Bank' are INVALID for ACCOUNT
############################################################# 

class BankAccount(PaymentAccountCommonInfo):
    user                = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    bank_name           = models.CharField(max_length=120)
    branch_name         = models.CharField(max_length=120)
    account_type        = models.CharField(max_length=50)
    account_holder_name = models.CharField(max_length=50)
    account_number      = models.CharField(max_length=50)
    routing_number      = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Bank Account"


class BkashAccount(PaymentAccountCommonInfo):
    user                = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    account_type        = models.CharField(max_length=50)
    account_holder_name = models.CharField(max_length=50)
    account_number      = PhoneNumberField()

    class Meta:
        verbose_name = "bKash Account"

    def __str__(self):
        return f"{self.account_number.as_e164}, {self.account_type}"
