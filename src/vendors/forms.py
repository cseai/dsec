from django import forms

from .models import Store

class RegisterStoreForm(forms.ModelForm):
    address_line_1  = forms.CharField(label='', max_length=120)
    address_line_2  = forms.CharField(label='', max_length=120, required=False)
    city            = forms.CharField(label='', max_length=120)
    state           = forms.CharField(label='', max_length=120)
    postal_code     = forms.CharField(label='', max_length=40)
    country         = forms.CharField(label='', max_length=50)
    
    address_line_1.widget.attrs.update({
        'placeholder': "Address line 1", 'title': 'Address line 1',
    })
    address_line_2.widget.attrs.update({
        'placeholder': "Address line 2", 'title': 'Address line 2 (Optional)',
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
        model= Store
        fields=('title', 'tagline', 'username', 'category', 'description', 'opening_time', 'closing_time', 'address_line_1', 'address_line_2', 'city', 'state', 'postal_code', 'country')

        # customize form attrs
        labels = {
            'title': '',
            'tagline': '',
            'username': '',
            'category': '',
            'description': '',
            'opening_time': '',
            'closing_time': '',
        }

        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': "Title",
                'required': True,
                'title': 'Store name',
            }),
            'tagline': forms.TextInput(attrs={
                'placeholder': "Tagline",
                'title': 'Store Tagline',
            }),
            'username': forms.TextInput(attrs={
                'placeholder': "username",
                'title': 'Unique Store username',
            }),
            'category': forms.Select(attrs={
                'class': 'form-control mb-30 custom-select',
                'style': 'height:50px ;border-radius:0px',
                'title': 'Store Category',
            }),
            'description': forms.Textarea(attrs={
                'placeholder': "Store Description",
                'title': 'Store description',
                'class':'form-control mb-30'
            }),
            'opening_time': forms.TimeInput(attrs={
                'placeholder': "Opening time. e.g. 8:00",
                'title': 'Store openning time',
            }),
            'closing_time': forms.TimeInput(attrs={
                'placeholder': "Closing time. e.g. 22:00",
                'title': 'Store closing time',
            }),
        }
    
    def save(self, commit=True):
        # Save the provided information
        store = super(RegisterStoreForm, self).save(commit=False)
        if commit:
            store.save()
        return store
    