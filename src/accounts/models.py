from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)
from phonenumber_field.modelfields import PhoneNumberField

from accounts.helpers import UploadTo


class UserManager(BaseUserManager):
    def create_user(self, phone, email=None, first_name=None, last_name=None, password=None, is_active=True, is_staff=False, is_admin=False):
        if not phone:
            raise ValueError("Users must have a phone number")
        if not password:
            raise ValueError("Users must have a password")
        user_obj = self.model(
            phone=phone,  # phone number should validate
            email=self.normalize_email(email) if email else email,
            first_name=first_name,
            last_name=last_name
        )
        user_obj.set_password(password)  # change user password
        user_obj.is_staff = is_staff
        user_obj.is_admin = is_admin
        user_obj.is_active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, phone, email=None, first_name=None, last_name=None, password=None):
        user = self.create_user(
            phone=phone,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self, phone, email=None, first_name=None, last_name=None, password=None):
        user = self.create_user(
            phone=phone,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            is_staff=True,
            is_admin=True
        )
        return user


class User(AbstractBaseUser):
    GENDER_MALE = 'M'
    GENDER_FEMALE = 'F'
    GENDER_OTHER = 'O'
    GENDER_CHOICES = [
        ('', 'Select Gender'),
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female'),
        (GENDER_OTHER, 'Other'),
    ]

    phone = PhoneNumberField(null=False, blank=False, unique=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        blank=True,
        null=True,
    )
    email = models.EmailField(max_length=255, blank=True, null=True)
    image = models.ImageField(
        default='accounts/user/image/default.png',
        upload_to=UploadTo('image', plus_id=True),
        null=True,
        blank=True,
        width_field="width_field",
        height_field="height_field"
    )
    height_field = models.IntegerField(default=0, null=True)
    width_field = models.IntegerField(default=0, null=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)  # can login
    is_staff = models.BooleanField(default=False)  # staff user non superuser
    is_admin = models.BooleanField(default=False)  # superuser
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'phone'  # username
    # USERNAME_FIELD and password are required by default
    REQUIRED_FIELDS = []  # ['first_name', 'last_name'] #python manage.py createsuperuser

    objects = UserManager()

    def __str__(self):
        return self.phone.as_e164

    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.phone.as_e164

    def get_short_name(self):
        return self.phone.as_e164

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
