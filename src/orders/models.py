from django.db import models
from django.contrib.auth import get_user_model
from addresses.models import Address

User = get_user_model()

class Order(models.Model):
    customer                = models.ForeignKey(User, related_name="customer", null=True, on_delete=models.SET_NULL)
    ordered_date            = models.DateTimeField(null=True, blank=True)
    date_confirmed          = models.DateTimeField(null=True, blank=True)
    shipping_date           = models.DateTimeField(null=True, blank=True)
    date_received           = models.DateTimeField(null=True, blank=True)
    quote                   = models.CharField(max_length=255, blank=True, null=True)
    confirmed_by            = models.ForeignKey(User, related_name="confirmed_by", null=True, blank=True, on_delete=models.SET_NULL)
    shipper                 = models.ForeignKey(User, related_name="shipper", null=True, blank=True, on_delete=models.SET_NULL)
    shipping_address        = models.ForeignKey(Address, related_name="shipping_address", null=True, blank=True, on_delete=models.SET_NULL)
    billing_address         = models.ForeignKey(Address, related_name="billing_address", null=True, blank=True, on_delete=models.SET_NULL)
    tracking_address        = models.ForeignKey(Address, related_name="tracking_address", null=True, blank=True, on_delete=models.SET_NULL)
    status                  = models.CharField(max_length=255, blank=True, null=True)
    is_pending              = models.BooleanField(default=True)
    is_aproved              = models.BooleanField(default=False)
    is_arrieved             = models.BooleanField(default=False)
    sub_total               = models.DecimalField(default=0.00, max_digits=20, decimal_places=2)
    shipping_total          = models.DecimalField(default=0.00, max_digits=20, decimal_places=2)
    total                   = models.DecimalField(default=0.00, max_digits=20, decimal_places=2)
    updated                 = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp               = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"order_id:{self.id}"

# class OrderItem(models.Model):
#     pass

