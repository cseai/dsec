from django.db import models
from taggit.managers import TaggableManager
# from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from vendors.models import Store

from accounts.helpers import UploadTo

# from PIL import Image

# User = get_user_model()

class Cuisine(models.Model):
    username                = models.CharField(max_length=20, unique=True, help_text="Unique cuisine username.")
    title                   = models.CharField(max_length=50, help_text="Cuisine title/name.")
    description             = models.TextField(null=True, blank=True, help_text="Describe about this Cuisine.")
    image                   = models.ImageField(
                                default='products/cuisine/image/default.png',
                                upload_to=UploadTo('image', plus_id=False),
                                null=True,
                                blank=True,
                                width_field="width_field",
                                height_field="height_field",
                                help_text="Photo of this Cuisine.",
                            )
    height_field            = models.IntegerField(default=0, null=True, help_text="Cuisine Photo's size (height) [Auto-captured]")
    width_field             = models.IntegerField(default=0, null=True, help_text="Cuisine Photo's size (weight) [Auto-captured]")
    active                  = models.BooleanField(default=True, help_text="Is this cuisine active?")
    updated                 = models.DateTimeField(auto_now=True, auto_now_add=False, help_text="Last updated timestamp.")
    timestamp               = models.DateTimeField(auto_now_add=True, help_text="Creation timestamp.")

    class Meta:
        verbose_name        = "cuisine"
        verbose_name_plural = "cuisines"

    def __str__(self):
        return self.title



class ProductManager(models.Manager):
    # we don't want to show inactive product
    # so that we are filtering that first in queryset
    def get_queryset(self):
        return super().get_queryset().filter(active=True)



class Product(models.Model):
    title                   = models.CharField(max_length=50, help_text="Product name/title.")
    store                   = models.ForeignKey(Store, null=True, on_delete=models.SET_NULL, help_text="Store reference [FK Store]")
    sku                     = models.CharField(max_length=20, null=True, blank=True, help_text="The SKU (Stock Keeping Unit) is composed of an alphanumeric combination of characters. The characters are a code that the price, product details, and the manufacturer.")
    description             = models.TextField(null=True, blank=True, help_text="Details about this product.")
    manufacturer            = models.CharField(max_length=40, null=True, blank=True, help_text="Manufacturer name/identity.")
    is_hot                  = models.BooleanField(default=False, help_text="Is this product most tending/popular/special?")
    sup_price               = models.DecimalField(default=0.00, max_digits=20, decimal_places=2, help_text="Product supply price.")
    selling_price           = models.DecimalField(default=0.00, max_digits=20, decimal_places=2, help_text="Product selling price.")
    discount                = models.DecimalField(default=0.00, max_digits=20, decimal_places=2, help_text="Product discount amount.")
    measuring_type          = models.CharField(max_length=40, null=True, blank=True, help_text="Measuring type of the product i.e Kg, Liter, Pice etc.")
    unit_in_stock           = models.DecimalField(default=0, max_digits=40, decimal_places=0, help_text="The amount of product in stock.")
    unit_on_order           = models.DecimalField(default=0, max_digits=40, decimal_places=0, help_text="The amount of product on order state [Auto updated].")
    cuisine                 = models.ForeignKey(Cuisine, null=True, on_delete=models.SET_NULL, help_text="Cuisine reference of this product.[FK Cuisine]")
    tags                    = TaggableManager(blank=True)
    is_available            = models.BooleanField(default=True, help_text="Is this product available?")
    is_discount_available   = models.BooleanField(default=False, help_text="Is the discount of this product available?")
    image                   = models.ImageField(
                                default='products/product/image/default.png',
                                upload_to=UploadTo('image', plus_id=True),
                                null=True,
                                blank=True,
                                width_field="width_field",
                                height_field="height_field",
                                help_text="Product image."
                            )
    height_field            = models.IntegerField(default=0, null=True, help_text="Product Photo's size (height) [Auto-captured]")
    width_field             = models.IntegerField(default=0, null=True, help_text="Product Photo's size (weight) [Auto-captured]")
    active                  = models.BooleanField(default=True, help_text="Is this product active?")
    updated                 = models.DateTimeField(auto_now=True, auto_now_add=False, help_text="Last updated timestamp.")
    timestamp               = models.DateTimeField(auto_now_add=True, help_text="Creation timestamp.")

    objects    = ProductManager() # custom manager for active product only

    class Meta:
        verbose_name        = "product"
        verbose_name_plural = "products"

    def __str__(self):
        return f"{self.title} @{self.store.username}"


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
    
    # def save(self,*args, **kwargs):
    #     super().save(*args, **kwargs)
    #     img = Image(self.image.path)
        
    #     if img.height > 300 and img.width > 300:
    #         output_size=(100,100)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)
