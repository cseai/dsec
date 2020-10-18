from django import forms

from .models import Store

class RegisterStoreForm(forms.Form):
    STORE_CATEGORY_CHOICES  = [
        ('', 'Select'),
        ('company', 'Company'),
        ('personal', 'Personal'),
        ('other', 'Other'),
    ]
    title           = forms.CharField(label='', max_length=150)
    category        = forms.ChoiceField(label='', widget=forms.Select(attrs={
                    'required': True,
                    'class': 'form-control mb-30 custom-select',
                    'style': 'height:50px ;border-radius:0px',
                    }),choices=STORE_CATEGORY_CHOICES)
    opening_time    = forms.TimeField(label='', required=False)
    closing_time    = forms.TimeField(label='', required=False)
    address_line_1  = forms.CharField(label='', max_length=120)
    address_line_2  = forms.CharField(label='', max_length=120, required=False)
    city            = forms.CharField(label='', max_length=120)
    state           = forms.CharField(label='', max_length=120)
    postal_code     = forms.CharField(label='', max_length=40)
    country         = forms.CharField(label='', max_length=50)

    title.widget.attrs.update({
        'placeholder': "Title", 'title': 'Store name', 'required': False,
    })
    opening_time.widget.attrs.update({
        'placeholder': "Opening time", 'title': 'When store opens...',
    })
    closing_time.widget.attrs.update({
        'placeholder': "Closing time", 'title': 'When store closes...',
    })
    address_line_1.widget.attrs.update({
        'placeholder': "Address line 1", 'title': 'Address line 1',
    })
    address_line_2.widget.attrs.update({
        'placeholder': "Address line 2", 'title': 'Address line 2',
    })
    city.widget.attrs.update({
        'placeholder': "City", 'title': 'City',
    })
    state.widget.attrs.update({
        'placeholder': "State", 'title': 'State',
    })
    postal_code.widget.attrs.update({
        'placeholder': "Postal code", 'title': 'Postal code',
    })
    country.widget.attrs.update({
        'placeholder': "Country", 'title': 'Country',
    })
    class Meta:
        model=Store
        fields=('title','category','opening_time', 'closing_time,''address_line_1','address_line_2','city','state','postal_code','country')
        labels = {
            'category':''
        }
        widgets={
            'category': forms.Select(attrs={
                    'required': True,
                    'class': 'form-control mb-30 custom-select',
                    'style': 'height:50px ;border-radius:0px',
                })
        }
        def __init__(self, *args, **kwargs):
            super(RegisterStoreForm, self).__init__(*args, **kwargs)
            self.fields['gender'].empty_label = "Select a Verb"
            # following line needed to refresh widget copy of choice list
            self.fields['gender'].widget.choices = self.fields['gender'].choices