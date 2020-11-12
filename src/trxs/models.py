from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth import get_user_model
from vendors.models import Store
from orders.models import Order
from express.models import Merchant

from .model_utils import TrxCommonInfo, TrxGenericRelation

User = get_user_model()


class StoreOrderTrx(TrxCommonInfo, TrxGenericRelation):
    store           = models.ForeignKey(Store, related_name='sot_store', null=True, on_delete=models.SET_NULL)
    order           = models.ForeignKey(Order, related_name='sot_order', null=True, on_delete=models.SET_NULL)
    
    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"ID:{self.id}, MANT:{self.amount}"


class VendorAdminTrx(TrxCommonInfo, TrxGenericRelation):
    admin_user      = models.ForeignKey(User, related_name='vat_admin_user', null=True, on_delete=models.SET_NULL)
    vendor_user     = models.ForeignKey(User, related_name='vat_vendor_user', null=True, on_delete=models.SET_NULL)
    store           = models.ForeignKey(Store, related_name='vat_store', null=True, on_delete=models.SET_NULL)
    
    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"ID:{self.id}, MANT:{self.amount}"


class MerchantAdminTrx(TrxCommonInfo, TrxGenericRelation):
    admin_user      = models.ForeignKey(User, related_name='mat_admin_user', null=True, on_delete=models.SET_NULL)
    merchant_user   = models.ForeignKey(User, related_name='mat_merchant_user', null=True, on_delete=models.SET_NULL)
    merchant        = models.ForeignKey(Merchant, related_name='mat_merchant', null=True, on_delete=models.SET_NULL)
    
    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"ID:{self.id}, MANT:{self.amount}"

