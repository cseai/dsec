from django.db import models
from django.contrib.auth import get_user_model

from addresses.models import Address

User = get_user_model()

class Profile(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    address     = models.ForeignKey(Address, null=True, on_delete=models.SET_NULL)
    is_active   = models.BooleanField(default=True)
    updated     = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        try:
            return self.user.get_full_name()
        except:
            return self.user.phone.as_e164
    