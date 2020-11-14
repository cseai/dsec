from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.contrib.auth import get_user_model

from addresses.models import Address

# Payment Accounts Models
from payment_accounts.models import (
    BankAccount,
    BkashAccount,
)

from phonenumber_field.modelfields import PhoneNumberField

User = get_user_model()



class Merchant(models.Model):
    CATEGORY_COMPANY            = 'C'
    CATEGORY_PERSONAL           = 'P'
    MERCHANT_CATEGORY_CHOICES   = [
        ('', 'Select Merchant category'),
        (CATEGORY_COMPANY, 'Company'),
        (CATEGORY_PERSONAL, 'Personal'),
    ]

    name                        = models.CharField(max_length=50)
    business_name               = models.CharField(max_length=50)
    username                    = models.CharField(max_length=20, unique=True)
    user                        = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    category                    = models.CharField(max_length=20, choices=MERCHANT_CATEGORY_CHOICES)
    parent                      = models.ForeignKey("self", blank=True, null=True, on_delete=models.SET_NULL)
    business_address            = models.ForeignKey(Address, related_name='merchant_business_address', null=True, on_delete=models.SET_NULL)
    pickup_address              = models.ForeignKey(Address, related_name='merchant_pickup_address', null=True, on_delete=models.SET_NULL)
    pickup_area                 = models.CharField(max_length=50)
    pickup_contact              = PhoneNumberField()
    business_email              = models.EmailField(blank=True, null=True)
    pickup_type                 = models.CharField(max_length=50)
    description                 = models.TextField(max_length=120, blank=True, null=True) # It does not validate max_length
    total_merchant_parcel_trx   = models.DecimalField(default=0.00, max_digits=30, decimal_places=2)
    total_merchant_admin_trx    = models.DecimalField(default=0.00, max_digits=30, decimal_places=2)
    is_verified                 = models.BooleanField(default=False)
    is_active                   = models.BooleanField(default=False)
    updated                     = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp                   = models.DateTimeField(auto_now_add=True)

    # payment_accounts
    payment_account_type        = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.CASCADE)
    payment_account_object_id   = models.PositiveIntegerField(null=True, blank=True)
    payment_account_object      = GenericForeignKey('payment_account_type', 'payment_account_object_id')
    

    class Meta:
        verbose_name            = "merchant"
        verbose_name_plural     = "merchants"

    def __str__(self):
        return f"@{self.username}:{self.business_name}"

    
    def get_express_merchant_detail_url(self):
        try:
            url = reverse("express:merchant_detail", kwargs={'merchant_username': self.username})
        except:
            url = '#merchant_detail'
        return url
    

    def get_express_merchant_update_url(self):
        try:
            url = reverse("express:merchant_update", kwargs={'merchant_username': self.username})
        except:
            url = '#merchant_update'
        return url


    def get_express_merchant_parcel_add_url(self):
        try:
            url = reverse("express:merchant_parcel_add", kwargs={'merchant_username': self.username})
        except:
            url = '#merchant_parcel_add'
        return url
    

    def get_express_merchant_parcel_list_url(self):
        try:
            url = reverse("express:merchant_parcel_list", kwargs={'merchant_username': self.username})
        except:
            url = '#merchant_parcel_list'
        return url



class Parcel(models.Model):
    merchant                    = models.ForeignKey(Merchant, null=True, on_delete=models.SET_NULL)
    customer_name               = models.CharField(max_length=50)
    customer_phone              = PhoneNumberField()
    cash_collection_amount      = models.DecimalField(default=0.00, max_digits=20, decimal_places=2)
    shipping_charge             = models.DecimalField(default=0.00, max_digits=20, decimal_places=2)
    delivery_area               = models.CharField(max_length=50)
    parcel_weight               = models.CharField(max_length=50)
    description                 = models.TextField(max_length=120, blank=True, null=True) # It does not validate max_length
    is_ordered                  = models.BooleanField(default=False)
    ordered_date                = models.DateTimeField(null=True, blank=True)
    date_confirmed              = models.DateTimeField(null=True, blank=True)
    shipping_date               = models.DateTimeField(null=True, blank=True)
    date_received               = models.DateTimeField(null=True, blank=True)
    quote                       = models.CharField(max_length=150, blank=True, null=True)
    confirmed_by                = models.ForeignKey(User, related_name="parcel_confirmed_by", null=True, blank=True, on_delete=models.SET_NULL)
    shipper                     = models.ForeignKey(User, related_name="parcel_shipper", null=True, blank=True, on_delete=models.SET_NULL)
    shipping_address            = models.ForeignKey(Address, related_name="parcel_shipping_address", null=True, blank=True, on_delete=models.SET_NULL)
    tracking_address            = models.ForeignKey(Address, related_name="parcel_tracking_address", null=True, blank=True, on_delete=models.SET_NULL)
    status                      = models.CharField(max_length=120, blank=True, null=True)
    is_pending                  = models.BooleanField(default=True)
    is_aproved                  = models.BooleanField(default=False)
    is_arrieved                 = models.BooleanField(default=False)
    updated                     = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp                   = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name            = "parcel"
        verbose_name_plural     = "parcels"

    def __str__(self):
        return f"ID:{self.id}, @{self.merchant.username} -> {self.shipping_address}"


    def get_express_merchant_parcel_detail_url(self):
        try:
            url = reverse("express:merchant_parcel_detail", kwargs={'merchant_username': self.merchant.username, 'parcel_id': self.id})
        except:
            url = '#parcel_detail'
        return url


    def get_express_merchant_parcel_update_url(self):
        try:
            url = reverse("express:merchant_parcel_update", kwargs={'merchant_username': self.merchant.username, 'parcel_id': self.id})
        except:
            url = '#parcel_update'
        return url
    

    def get_express_merchant_parcel_remove_url(self):
        try:
            url = reverse("express:merchant_parcel_remove", kwargs={'merchant_username': self.merchant.username, 'parcel_id': self.id})
        except:
            url = '#parcel_remove'
        return url