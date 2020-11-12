from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class TrxGenericRelation(models.Model):
    content_type    = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id       = models.PositiveIntegerField()
    content_object  = GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True



class TrxCommonInfo(models.Model):
    amount          = models.DecimalField(editable=False, default=0.00, max_digits=20, decimal_places=2)
    message         = models.CharField(editable=False, max_length=200, null=True, blank=True)
    timestamp       = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
