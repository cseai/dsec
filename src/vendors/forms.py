from django import forms

from .models import Store

class RegisterStoreForm(forms.Form):
    STORE_CATEGORY_CHOICES  = [
        ('company', 'Company'),
        ('personal', 'Personal'),
        ('other', 'Other'),
    ]
    title           = forms.CharField(label='', max_length=150)
    category        = forms.ChoiceField(choices=STORE_CATEGORY_CHOICES)
    opening_time    = forms.TimeField(label='')
    closing_time    = forms.TimeField(label='')
    address_line_1  = forms.CharField(label='', max_length=120)
    address_line_2  = forms.CharField(label='', max_length=120)
    city            = forms.CharField(label='', max_length=120)
    state           = forms.CharField(label='', max_length=120)
    postal_code     = forms.CharField(label='', max_length=40)
    country         = forms.CharField(label='', max_length=50)