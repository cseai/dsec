from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from addresses.models import Address

from accounts.helpers import UploadTo

User = get_user_model()


class Store(models.Model):
    CATEGORY_COMPANY        = 'C'
    CATEGORY_PERSONAL       = 'P'
    STORE_CATEGORY_CHOICES  = [
        ('', 'Select store category'),
        (CATEGORY_COMPANY, 'Company'),
        (CATEGORY_PERSONAL, 'Personal'),
    ]
    title                   = models.CharField(max_length=50)
    tagline                 = models.CharField(max_length=50, blank=True, null=True)
    username                = models.CharField(max_length=20, unique=True)
    user                    = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    category                = models.CharField(max_length=20, choices=STORE_CATEGORY_CHOICES)
    parent                  = models.ForeignKey("self", blank=True, null=True, on_delete=models.SET_NULL)
    description             = models.TextField(max_length=120, blank=True, null=True) # It does not validate max_length
    opening_time            = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    closing_time            = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    # store_status            = models.CharField(max_length=255, blank=True, null=True)
    is_open                 = models.BooleanField(default=False)
    off_days                = models.CharField(max_length=30, blank=True, null=True)
    address                 = models.ForeignKey(Address, null=True, on_delete=models.SET_NULL) # always parmanent address
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
    is_verified             = models.BooleanField(default=False)
    is_active               = models.BooleanField(default=False)
    updated                 = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp               = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = "store"
        verbose_name_plural = "stores"

    def __str__(self):
        return f"{self.title}[@{self.username}]"
    

    def get_store_detail_url(self):
        try:
            url = reverse("stores:store_detail", kwargs={'store_username': self.username})
        except:
            url = '#store_detail'
        return url

    
    def get_vendor_store_detail_url(self):
        try:
            url = reverse("vendors:store_detail", kwargs={'store_username': self.username})
        except:
            url = '#store_detail'
        return url
    

    def get_vendor_store_update_url(self):
        try:
            url = reverse("vendors:store_update", kwargs={'store_username': self.username})
        except:
            url = '#store_update'
        return url


    def get_vendor_store_product_add_url(self):
        try:
            url = reverse("vendors:store_product_add", kwargs={'store_username': self.username})
        except:
            url = '#store_product_add'
        return url