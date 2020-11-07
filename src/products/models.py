from django.db import models
# from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from vendors.models import Store

from accounts.helpers import UploadTo

# User = get_user_model()

class ProductManager(models.Manager):
    # we don't want to show inactive product
    # so that we are filtering that first in queryset
    def get_queryset(self):
        return super().get_queryset().filter(active=True)



class Product(models.Model):
    title                   = models.CharField(max_length=50)
    store                   = models.ForeignKey(Store, null=True, on_delete=models.SET_NULL)
    sku                     = models.CharField(max_length=20, null=True, blank=True)
    description             = models.TextField(null=True, blank=True)
    manufacturer            = models.CharField(max_length=40, null=True, blank=True)
    is_hot                  = models.BooleanField(default=False)
    sup_price               = models.DecimalField(default=0.00, max_digits=20, decimal_places=2)
    selling_price           = models.DecimalField(default=0.00, max_digits=20, decimal_places=2)
    discount                = models.DecimalField(default=0.00, max_digits=20, decimal_places=2)
    measuring_type          = models.CharField(max_length=40, null=True, blank=True)
    unit_in_stock           = models.DecimalField(default=0, max_digits=40, decimal_places=0)
    unit_on_order           = models.DecimalField(default=0, max_digits=40, decimal_places=0)
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
    active                  = models.BooleanField(default=True)
    updated                 = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp               = models.DateTimeField(auto_now_add=True)

    objects    = ProductManager() # custom manager for active product only

    class Meta:
        verbose_name        = "product"
        verbose_name_plural = "products"

    def __str__(self):
        return self.title


    def get_store_product_detail_url(self):
        try:
            url = reverse("stores:store_product_detail", kwargs={'store_username': self.store.username, 'product_id': self.id})
        except:
            url = '#product_detail'
        return url


    def get_vendor_store_product_detail_url(self):
        try:
            url = reverse("vendors:store_product_detail", kwargs={'store_username': self.store.username, 'product_id': self.id})
        except:
            url = '#product_detail'
        return url


    def get_vendor_store_product_update_url(self):
        try:
            url = reverse("vendors:store_product_update", kwargs={'store_username': self.store.username, 'product_id': self.id})
        except:
            url = '#product_update'
        return url
    

    def get_vendor_store_product_remove_url(self):
        try:
            url = reverse("vendors:store_product_remove", kwargs={'store_username': self.store.username, 'product_id': self.id})
        except:
            url = '#product_remove'
        return url
