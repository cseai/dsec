from django.db import models
from django.contrib.auth import get_user_model
from vendors.models import Store
from orders.models import Order

User = get_user_model()


class StoreOrderTrx(models.Model):
    store                   = models.ForeignKey(Store, null=True, on_delete=models.SET_NULL)
    order                   = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL)
    amount                  = models.DecimalField(default=0.00, max_digits=20, decimal_places=2)
    timestamp               = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.store and self.store.title:
            return f"ID:{self.id}, S:{self.store.title}, AMNT:{self.amount}"
        return f"ID:{self.id}, AMNT:{self.amount}"


class VendorAdminTrx(models.Model):
    admin_user              = models.ForeignKey(User, related_name="admin_user", null=True, on_delete=models.SET_NULL)
    vendor_user             = models.ForeignKey(User, related_name="vendor_user", null=True, on_delete=models.SET_NULL)
    store                   = models.ForeignKey(Store, null=True, on_delete=models.SET_NULL)
    vouchar_amount          = models.DecimalField(default=0.00, max_digits=20, decimal_places=2)
    timestamp               = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.store and self.store.title:
            return f"ID:{self.id}, S:{self.store.title}, AMNT:{self.vouchar_amount}"
        return f"ID:{self.id}, AMNT:{self.vouchar_amount}"