from django.db import models
from model_utils import FieldTracker

class PaymentAccountCommonInfo(models.Model):
    is_verified         = models.BooleanField(default=False)
    is_active           = models.BooleanField(default=False)
    updated             = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp           = models.DateTimeField(auto_now_add=True)
    # to track field changes using FieldTracker
    tracker             = FieldTracker()

    class Meta:
        abstract = True
