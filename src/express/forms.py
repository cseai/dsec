from django import forms
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType
from express.models import Merchant
from express.models import Parcel
from addresses.models import  Address

class ImagePreviewWidget(forms.widgets.FileInput):
    def render(self, name, value, attrs=None, **kwargs):
        input_html = super().render(name, value, attrs=None, **kwargs)
        img_html = mark_safe(f'<br><br><img src="{value.url}" style="height:200px; width:200px; margin:0 auto; display:flex; " id="imgUploadProduct"  /><br><br>')
        return f'{img_html}{input_html}'


class RegisterMerchantForm(forms.ModelForm):
    class Meta:
        model= Merchant
        fields=('name', 'business_name', 'username', 'category', 'pickup_area', 'pickup_contact', 'business_email', 'pickup_type', 'description')

    def save(self, commit=True):
        # Save the provided information
        merchant = super(RegisterMerchantForm, self).save(commit=False)
        if commit:
            merchant.save()
        return merchant


class MerchantUpdateForm(forms.ModelForm):
    class Meta:
        model= Merchant
        fields=('name', 'business_name', 'username', 'category', 'pickup_area', 'pickup_contact', 'business_email', 'pickup_type', 'description', 'payment_account_type',)
    
    def __init__(self, *args, **kwargs):
        super(MerchantUpdateForm, self).__init__(*args, **kwargs)
        self.fields['payment_account_type'].queryset = ContentType.objects.filter(app_label='payment_accounts', model__iendswith='Account')


    def save(self, commit=True):
        # Save the provided information
        merchant = super(MerchantUpdateForm, self).save(commit=False)
        if commit:
            merchant.save()
        return merchant


class MerchantAddressUpdateForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('line_1', 'line_2', 'city', 'state', 'postal_code', 'country',)
        labels = {
            'line_1': "Address line 1", 
            'line_2': "Address line 2", 
            'city': "City",
            'state': "State",
            'postal_code': "Postal code",
            'country': "Country",
        }
        widgets = {
            # 'address_type': forms.Select(attrs={
            #     'class': 'form-control mb-30 custom-select',
            #     'style': 'height:50px ;border-radius:0px',
            #     'title': 'Address type',
            #     'disabled': True,
            #     # 'required': False,
            # }),
            'line_1': forms.TextInput(attrs={
                'placeholder': "Address line 1",
                'title': 'Address line 1',
            }),
            'line_2': forms.TextInput(attrs={
                'placeholder': "Address line 2",
                'title': 'Address line 2',
            }),
            'city': forms.Select(attrs={
                'placeholder': "City",
                'title': 'City',
            }),
            'state': forms.Select(attrs={
                'placeholder': "State",
                'title': 'State',
            }),
            'postal_code': forms.TextInput(attrs={
                'placeholder': "Postal code",
                'title': 'Postal code',
            }),
            'country': forms.Select(attrs={
                'placeholder': "Country",
                'title': 'Country',
            }),
        }

    def save(self, commit=True):
        # Save the provided information
        store_address = super(MerchantAddressUpdateForm, self).save(commit=False)
        if commit:
            store_address.save()
        return store_address


class MerchantParcelAddForm(forms.ModelForm):
    class Meta:
        model = Parcel
        fields = ('customer_name', 'customer_phone', 'cash_collection_amount', 'delivery_area', 'parcel_weight', 'description', 'is_ordered', 'quote',)

    
    def save(self, commit=True):
        # Save the provided information
        merchant_parcel = super(MerchantParcelAddForm, self).save(commit=False)
        if commit:
            merchant_parcel.save()
        return merchant_parcel



class MerchantParcelUpdateForm(forms.ModelForm):
    class Meta:
        model = Parcel
        fields = ('customer_name', 'customer_phone', 'cash_collection_amount', 'delivery_area', 'parcel_weight', 'description', 'is_ordered', 'quote',)


    def save(self, commit=True):
        # Save the provided information
        merchant_parcel = super(MerchantParcelUpdateForm, self).save(commit=False)
        if commit:
            merchant_parcel.save()
        return merchant_parcel


class MerchantParcelRemoveForm(forms.ModelForm):
    confirm_remove = forms.BooleanField()
    class Meta:
        model = Parcel
        fields = ('confirm_remove',)

    def save(self, commit=True):
        # Save the provided information
        merchant_parcel = super(MerchantParcelRemoveForm, self).save(commit=False)
        # may be we should to delete this object after checking
        if commit:
            merchant_parcel.save()
        return merchant_parcel