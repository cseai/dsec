from django import forms

from .models import Store
from addresses.models import  Address
from products.models import Product

class RegisterStoreForm(forms.ModelForm):
    address_line_1  = forms.CharField(label='', max_length=120)
    address_line_2  = forms.CharField(label='', max_length=120, required=False)
    city            = forms.ChoiceField(label='', choices=Address.CITY_CHOICES)
    state           = forms.ChoiceField(label='', choices=Address.STATE_CHOICES)
    postal_code     = forms.CharField(label='', max_length=10)
    country         = forms.ChoiceField(label='', choices=Address.COUNTRY_CHOICES)
    
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


class StoreUpdateForm(forms.ModelForm):
    class Meta:
        model= Store
        fields=('title', 'tagline', 'username', 'category', 'logo', 'description', 'opening_time', 'closing_time', 'is_open', )

        # customize form attrs
        # labels = {
        #     # 'title': '',
        #     # 'tagline': '',
        #     # 'username': '',
        #     # 'category': '',
        #     # 'description': '',
        #     # 'opening_time': '',
        #     # 'closing_time': '',
        #     # 'is_open': ''
        # }

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
        store = super(StoreUpdateForm, self).save(commit=False)
        if commit:
            store.save()
        return store


class StoreAddressUpdateForm(forms.ModelForm):
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
        store_address = super(StoreAddressUpdateForm, self).save(commit=False)
        if commit:
            store_address.save()
        return store_address


class StoreStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ('is_open',)

        # labels = {
        #     'is_open': "Open or Close", 
        # }
        # widgets = {
        #     'is_open': forms.TextInput(attrs={
        #         'placeholder': "e.g. Open/Close",
        #         'title': 'Current Store Status',
        #         'required': True,
        #     }),
        # }
    
    def save(self, commit=True):
        # Save the provided information
        store = super(StoreStatusUpdateForm, self).save(commit=False)
        if commit:
            store.save()
        return store



class StoreProductAddForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('title', 'sku', 'description', 'manufacturer', 'is_hot', 'sup_price', 'selling_price', 'discount', 'measuring_type', 'unit_in_stock', 'unit_on_order', 'category', 'is_available', 'is_discount_available', 'image',)

        # customize form attrs
        labels = {
            'title': "Product Title",
            'sku': "SKU",
            'description': "Description",
            'manufacturer': "Manufacturer",
            'is_hot': "Is hot",
            'sup_price': "Supply Price (BDT)", 
            'selling_price': "Selling Price (BDT)", 
            'discount': "Discount", 
            'measuring_type': "Measuring Type", 
            'unit_in_stock': "Quantity in stock", 
            'unit_on_order': "Quantity on order", 
            'category': "Product Category", 
            # 'is_available': "", 
            # 'is_discount_available': "", 
            # 'image': "",
        }

        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': "Product Title",
                'title': 'Product Title',
                'required': True,
            }),
            'sku': forms.TextInput(attrs={
                'placeholder': "SKU",
                'title': 'SKU',
            }),
            'description': forms.Textarea(attrs={
                'placeholder': "Product Description",
                'title': 'Product description',
                'required': True,
            }),
            'manufacturer': forms.TextInput(attrs={
                'placeholder': "Manufacturer",
                'title': 'Manufacturer Name',
            }),
            'measuring_type': forms.TextInput(attrs={
                'placeholder': "E.g. Kg/Litter/Pices/Meter etc.",
                'title': 'E.g. Kg/Litter/Pices/Meter etc.',
                'required': True,
            }),
            'category': forms.TextInput(attrs={
                'placeholder': "Product Category/Tag. E.g: Pizza",
                'title': 'Product Category/Tag',
            }),
        }


    def save(self, commit=True):
        # Save the provided information
        store_product = super(StoreProductAddForm, self).save(commit=False)
        if commit:
            store_product.save()
        return store_product



class StoreProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('title', 'sku', 'description', 'manufacturer', 'is_hot', 'sup_price', 'selling_price', 'discount', 'measuring_type', 'unit_in_stock', 'unit_on_order', 'category', 'is_available', 'is_discount_available', 'image',)

        # customize form attrs
        labels = {
            'title': "Product Title",
            'sku': "SKU",
            'description': "Description",
            'manufacturer': "Manufacturer",
            'is_hot': "Is hot",
            'sup_price': "Supply Price (BDT)", 
            'selling_price': "Selling Price (BDT)", 
            'discount': "Discount", 
            'measuring_type': "Measuring Type", 
            'unit_in_stock': "Quantity in stock", 
            'unit_on_order': "Quantity on order", 
            'category': "Product Category", 
            # 'is_available': "", 
            # 'is_discount_available': "", 
            # 'image': "",
        }

        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': "Product Title",
                'title': 'Product Title',
                'required': True,
            }),
            'sku': forms.TextInput(attrs={
                'placeholder': "SKU",
                'title': 'SKU',
            }),
            'description': forms.Textarea(attrs={
                'placeholder': "Product Description",
                'title': 'Product description',
                'required': True,
            }),
            'manufacturer': forms.TextInput(attrs={
                'placeholder': "Manufacturer",
                'title': 'Manufacturer Name',
            }),
            'measuring_type': forms.TextInput(attrs={
                'placeholder': "E.g. Kg/Litter/Pices/Meter etc.",
                'title': 'E.g. Kg/Litter/Pices/Meter etc.',
                'required': True,
            }),
            'category': forms.TextInput(attrs={
                'placeholder': "Product Category/Tag. E.g: Pizza",
                'title': 'Product Category/Tag',
            }),
        }


    def save(self, commit=True):
        # Save the provided information
        store_product = super(StoreProductUpdateForm, self).save(commit=False)
        if commit:
            store_product.save()
        return store_product



class StoreProductRemoveForm(forms.ModelForm):
    confirm_remove = forms.BooleanField()
    class Meta:
        model = Product
        fields = ('confirm_remove',)
    


    def save(self, commit=True):
        # Save the provided information
        store_product = super(StoreProductRemoveForm, self).save(commit=False)
        store_product.active = False
        store_product.is_available = False
        if commit:
            store_product.save()
        return store_product