from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth import get_user_model
from vendors.models import Store
from orders.models import Order
from express.models import Merchant

from .model_utils import TrxCommonInfo

User = get_user_model()


class StoreOrderTrx(TrxCommonInfo):
    store           = models.ForeignKey(Store, related_name='sot_store', null=True, on_delete=models.SET_NULL)
    order           = models.ForeignKey(Order, related_name='sot_order', null=True, on_delete=models.SET_NULL)
    
    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"ID:{self.id}, MANT:{self.amount}"


class VendorAdminTrx(TrxCommonInfo):
    admin_user      = models.ForeignKey(User, related_name='vat_admin_user', null=True, on_delete=models.SET_NULL)
    vendor_user     = models.ForeignKey(User, related_name='vat_vendor_user', null=True, on_delete=models.SET_NULL)
    store           = models.ForeignKey(Store, related_name='vat_store', null=True, on_delete=models.SET_NULL)
    
    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"ID:{self.id}, MANT:{self.amount}"


class MerchantAdminTrx(TrxCommonInfo):
    admin_user      = models.ForeignKey(User, related_name='mat_admin_user', null=True, on_delete=models.SET_NULL)
    merchant_user   = models.ForeignKey(User, related_name='mat_merchant_user', null=True, on_delete=models.SET_NULL)
    merchant        = models.ForeignKey(Merchant, related_name='mat_merchant', null=True, on_delete=models.SET_NULL)
    
    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"ID:{self.id}, AMNT:{self.amount}"








"""
from django.db import models
from django.contrib.auth import get_user_model
from vendors.models import Store
from orders.models import Order

User = get_user_model()


class StoreOrderTrx(models.Model):
    store                   = models.ForeignKey(Store, null=True, on_delete=models.SET_NULL)
    order                   = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL)
    amount                  = models.DecimalField(default=0.00, max_digits=20, decimal_places=2)
    # TRX should not update but we want to keep track if something happen or forcely update
    updated                 = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp               = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = "store-order transaction"
        verbose_name_plural = "store-order transactions"

    def __str__(self):
        if self.store and self.store.title:
            return f"ID:{self.id}, S:{self.store.title}, AMNT:{self.amount}"
        return f"ID:{self.id}, AMNT:{self.amount}"


class VendorAdminTrx(models.Model):
    admin_user              = models.ForeignKey(User, related_name="admin_user", null=True, on_delete=models.SET_NULL)
    vendor_user             = models.ForeignKey(User, related_name="vendor_user", null=True, on_delete=models.SET_NULL)
    store                   = models.ForeignKey(Store, null=True, on_delete=models.SET_NULL)
    vouchar_amount          = models.DecimalField(default=0.00, max_digits=20, decimal_places=2)
    # TRX should not update but we want to keep track if something happen or forcely update
    updated                 = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp               = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = "vendor-admin transaction"
        verbose_name_plural = "vendor-admin transactions"

    def __str__(self):
        if self.store and self.store.title:
            return f"ID:{self.id}, S:{self.store.title}, AMNT:{self.vouchar_amount}"
        return f"ID:{self.id}, AMNT:{self.vouchar_amount}"
"""