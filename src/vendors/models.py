from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from addresses.models import Address
from accounts.helpers import UploadTo

from PIL import Image

User = get_user_model()

# verbose_name='user',related_name='store',
class Store(models.Model):
    CATEGORY_COMPANY        = 'C'
    CATEGORY_PERSONAL       = 'P'
    STORE_CATEGORY_CHOICES  = [
        ('', 'Select store category'),
        (CATEGORY_COMPANY, 'Company'),
        (CATEGORY_PERSONAL, 'Personal'),
    ]
    title                   = models.CharField(max_length=50, help_text="Store/Restaurant's name/title.")
    tagline                 = models.CharField(max_length=50, blank=True, null=True, help_text="Store/Restaurant's tagline.")
    username                = models.CharField(max_length=20, unique=True, help_text="Store's unique username.")
    user                    = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, help_text="Store's owner (User FK).")
    category                = models.CharField(max_length=20, choices=STORE_CATEGORY_CHOICES)
    parent                  = models.ForeignKey("self", blank=True, null=True, on_delete=models.SET_NULL, help_text="If this store is under a company and has superior/parent store/company then this is the reference of that parent/company store. Otherwise it's not applicable.")
    description             = models.TextField(max_length=120, blank=True, null=True, help_text="Describe about your store/services/products etc.") # It does not validate max_length
    opening_time            = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True, help_text="Generally the time when services are started.")
    closing_time            = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True, help_text="Generally the time when services are ended.")
    # store_status            = models.CharField(max_length=255, blank=True, null=True)
    is_open                 = models.BooleanField(default=False, help_text="is the Store/Restaurant open?")
    off_days                = models.CharField(max_length=30, blank=True, null=True, help_text="Off days in a week. E.g. FRI, SAT")
    address                 = models.ForeignKey(Address, null=True, on_delete=models.SET_NULL, help_text="Address of the Store/Restaurant (Address FK).") # always parmanent address
    logo                    = models.ImageField(
                                default='vendors/store/logo/default.png',
                                upload_to=UploadTo('logo', plus_id=True),
                                null=True,
                                blank=True,
                                width_field="width_field",
                                height_field="height_field",
                                help_text="Store/Restaurant's Logo/Profile Photo"
                            )
    height_field            = models.IntegerField(default=0, null=True, help_text="Store/Restaurant's Logo/Profile Photo's size (height) [Auto-captured]")
    width_field             = models.IntegerField(default=0, null=True, help_text="Store/Restaurant's Logo/Profile Photo's size (weight) [Auto-captured]")
    total_store_order_trx   = models.DecimalField(default=0.00, max_digits=30, decimal_places=2, help_text="Total transaction amount between Store and Order/Customer. [Automatic Process]")
    total_vendor_admin_trx  = models.DecimalField(default=0.00, max_digits=30, decimal_places=2, help_text="Total transaction amount between Vendor and Admin. [Automatic Process]")
    is_verified             = models.BooleanField(default=False, help_text="Is this Vendor/Store/Restaurant account verified?")
    is_active               = models.BooleanField(default=False, help_text="Is this Vendor/Store/Restaurant account active?")
    updated                 = models.DateTimeField(auto_now=True, auto_now_add=False, help_text="Last updated timestamp.")
    timestamp               = models.DateTimeField(auto_now_add=True, help_text="Creation timestamp.")

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
    
    