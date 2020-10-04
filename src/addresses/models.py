from django.db import models

class Address(models.Model):
    ADDRESS_TYPE_PARMANENT  = 'parmanent'
    ADDRESS_TYPE_MAILING    = 'mailing'
    ADDRESS_TYPE_BILLING    = 'billing'
    ADDRESS_TYPE_SHIPPING   = 'shipping'
    ADDRESS_TYPE_CHOICES    = [
        (ADDRESS_TYPE_PARMANENT, 'Parmanent Address'),
        (ADDRESS_TYPE_MAILING, 'Mailing Address'),
        (ADDRESS_TYPE_BILLING, 'Billing Address'),
        (ADDRESS_TYPE_SHIPPING, 'Shipping Address'),
    ]

    address_type        = models.CharField(max_length=10, choices=ADDRESS_TYPE_CHOICES)
    line_1              = models.CharField(max_length=120)
    line_2              = models.CharField(max_length=120, null=True, blank=True)
    city                = models.CharField(max_length=120)
    state               = models.CharField(max_length=120)
    postal_code         = models.CharField(max_length=40)
    country             = models.CharField(max_length=50, default='Bangladesh')
    timestamp           = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.line_1},{self.city}-{self.postal_code}"

