from django.contrib import admin

from .models import (
    StoreOrderTrx,
    VendorAdminTrx,
    MerchantAdminTrx,
)

admin.site.register(StoreOrderTrx)
admin.site.register(VendorAdminTrx)
admin.site.register(MerchantAdminTrx)