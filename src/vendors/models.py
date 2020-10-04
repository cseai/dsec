from django.db import models
from django.contrib.auth import get_user_model
from addresses.models import Address

from accounts.helpers import UploadTo

User = get_user_model()


class Store(models.Model):
    STORE_CATEGORY_CHOICES  = [
        ('company', 'Company'),
        ('personal', 'Personal'),
        ('other', 'Other'),
    ]
    title                   = models.CharField(max_length=255)
    user                    = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    category                = models.CharField(max_length=20, choices=STORE_CATEGORY_CHOICES)
    parent                  = models.ForeignKey("self", blank=True, null=True, on_delete=models.SET_NULL)
    opening_time            = models.CharField(max_length=50, blank=True, null=True)
    closing_time            = models.CharField(max_length=50, blank=True, null=True)
    store_status            = models.CharField(max_length=255, blank=True, null=True)
    address                 = models.ForeignKey(Address, null=True, on_delete=models.SET_NULL)
    logo                    = models.ImageField(
                                default='vendors/store/logo/default.png',
                                upload_to=UploadTo('logo', plus_id=True),
                                null=True,
                                blank=True,
                                width_field="width_field",
                                height_field="height_field"
                            )
    height_field            = models.IntegerField(default=0, null=True)
    width_field             = models.IntegerField(default=0, null=True)
    total_store_order_trx   = models.DecimalField(default=0.00, max_digits=30, decimal_places=2)
    total_vendor_admin_trx  = models.DecimalField(default=0.00, max_digits=30, decimal_places=2)
    is_active               = models.BooleanField(default=True)
    updated                 = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp               = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"
