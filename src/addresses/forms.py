from django import forms

from .models import Address

class AddressUpdateForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('address_type', 'line_1', 'line_2', 'city', 'state', 'postal_code', 'country')
        widgets = {
            'address_type': forms.Select(attrs={
                'class': 'form-control mb-30 custom-select',
                'style': 'height:50px ;border-radius:0px',
                'title': 'Address type',
            }),
            'line_1': forms.TextInput(attrs={
                # 'placeholder': "Address line 1",
                'title': 'Address line 1',
            }),
            'line_2': forms.TextInput(attrs={
                # 'placeholder': "Address line 2",
                'title': 'Address line 2',
            }),
            'city': forms.TextInput(attrs={
                # 'placeholder': "City",
                'title': 'City',
            }),
            'state': forms.TextInput(attrs={
                # 'placeholder': "State",
                'title': 'State',
            }),
            'postal_code': forms.TextInput(attrs={
                # 'placeholder': "Postal code",
                'title': 'Postal code',
            }),
            'country': forms.TextInput(attrs={
                # 'placeholder': "Country",
                'title': 'Country',
            }),
        }

    
    def save(self, commit=True):
        address = super(AddressUpdateForm, self).save(commit=False)
        if commit:
            address.save()
        return address
