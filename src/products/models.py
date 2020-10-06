from django.db import models
# from django.contrib.auth import get_user_model
from vendors.models import Store

from accounts.helpers import UploadTo

# User = get_user_model()

class Product(models.Model):
    title                   = models.CharField(max_length=255)
    store                   = models.ForeignKey(Store, null=True, on_delete=models.SET_NULL)
    sku                     = models.CharField(max_length=100, null=True, blank=True)
    description             = models.TextField(null=True, blank=True)
    manufacturer            = models.CharField(max_length=100, null=True, blank=True)
    # margin                  = 
    is_hot                  = models.BooleanField(default=False)
    sup_price               = models.DecimalField(default=0.00, max_digits=20, decimal_places=2)
    selling_price           = models.DecimalField(default=0.00, max_digits=20, decimal_places=2)
    discount                = models.DecimalField(default=0.00, max_digits=20, decimal_places=2)
    measuring_type          = models.CharField(max_length=50, null=True, blank=True)
    unit_in_stock           = models.DecimalField(default=0.00, max_digits=40, decimal_places=2)
    unit_on_order           = models.DecimalField(default=0.00, max_digits=40, decimal_places=2)
    category                = models.CharField(max_length=100, null=True, blank=True)
    is_available            = models.BooleanField(default=True)
    is_discount_available   = models.BooleanField(default=False)
    image                   = models.ImageField(
                                default='products/product/image/default.png',
                                upload_to=UploadTo('image', plus_id=True),
                                null=True,
                                blank=True,
                                width_field="width_field",
                                height_field="height_field"
                            )
    height_field            = models.IntegerField(default=0, null=True)
    width_field             = models.IntegerField(default=0, null=True)
    # more_images             = 
    updated                 = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp               = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = "product"
        verbose_name_plural = "products"

    def __str__(self):
        return self.title