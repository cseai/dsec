from django import forms
from django.contrib.auth import get_user_model

from phonenumber_field.formfields import PhoneNumberField
import phonenumbers

User = get_user_model()

class RequsetRegisterForm(forms.Form):
    # step = 1
    step = forms.IntegerField(min_value=1, max_value=3)
    phone = forms.CharField(label='')
    
    phone.widget.attrs.update({
        'placeholder': "Phone", 'title': 'Phone number (BD)'
    })

    def __init__(self, *args, **kwargs):
        super(RequsetRegisterForm, self).__init__(*args, **kwargs)
        self.fields['step'].widget = forms.HiddenInput()
        self.fields['step'].initial = 1 #step_number

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        # check is it a valid BD phone number
        try:
            phone_instance = phonenumbers.parse(phone, "BD")
            if not phonenumbers.is_possible_number(phone_instance):
                raise forms.ValidationError("Invalid phone number ")
                # (is_possible_number: False)
            if not phonenumbers.is_valid_number(phone_instance):
                raise forms.ValidationError("Invalid phone number ")
                # (is_possible_number: False)
        except phonenumbers.phonenumberutil.NumberParseException:
            raise forms.ValidationError("Invalid phone number")
        phone_as_e164 = phonenumbers.format_number(phone_instance, phonenumbers.PhoneNumberFormat.E164)
        # return phone_instance
        print(f'phone_as_e164:{phone_as_e164}')

        # check is it (account of this phone) already exist or not
        existed_user = User.objects.filter(phone=phone_instance).first()
        if existed_user:
            raise forms.ValidationError("Account already exist! Try another phone or login.")

        return phone_as_e164


class OTPRegisterForm(forms.Form):
    # step = 2
    step = forms.IntegerField(min_value=1, max_value=3)
    # phone = forms.CharField(label='', disabled=True)
    phone = forms.CharField(label='')
    security_code = forms.CharField(label='', required=True)

    phone.widget.attrs.update({
        'placeholder': "Phone", 'title': 'Phone number (BD)'
    })
    security_code.widget.attrs.update({
        'placeholder': "Security code", 'title': 'Security code (OTP)',
    })

    def __init__(self, *args, **kwargs):
        super(OTPRegisterForm, self).__init__(*args, **kwargs)
        self.fields['step'].widget = forms.HiddenInput()
        self.fields['step'].initial = 2 #step_number
    
    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        try:
            phone_instance = phonenumbers.parse(phone, "BD")
            if not phonenumbers.is_possible_number(phone_instance):
                raise forms.ValidationError("Invalid phone number ")
                # (is_possible_number: False)
            if not phonenumbers.is_valid_number(phone_instance):
                raise forms.ValidationError("Invalid phone number ")
                # (is_possible_number: False)
        except phonenumbers.phonenumberutil.NumberParseException:
            raise forms.ValidationError("Invalid phone number")
        # print(phone_instance)
        phone_as_e164 = phonenumbers.format_number(phone_instance, phonenumbers.PhoneNumberFormat.E164)
        # return phone_instance
        return phone_as_e164
    
    def clean_security_code(self):
        security_code = self.cleaned_data.get("security_code")
        if len(security_code) != 6:
            raise forms.ValidationError("Invalid security code!")
        if not str(security_code).isdigit:
            raise forms.ValidationError("Invalid security code!")
        
        return security_code


class VerifiedRegisterForm(forms.ModelForm):
    # step = 3
    step = forms.IntegerField(min_value=1, max_value=3)
    # phone = forms.CharField(label='', disabled=True)
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={
        'placeholder': "Password"
    }))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={
        'placeholder': "Password confirmation"
    }))
    # is_verified = forms.BooleanField(label='', disabled=True)

    class Meta:
        model = User
        fields = ('phone', 'first_name', 'last_name', 'gender', 'email', 'is_verified',)
        # customize form attrs
        labels = {
            'first_name': '',
            'last_name': '',
            'email': '',
            'gender': '',
        }

        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': "First name",
                'required': True,
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': "Last name",
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': "Email",
                'required': False,
            }),
            'gender': forms.Select(attrs={
                'required': True,
                'class': 'form-control mb-30 custom-select',
                'style': 'height:50px ;border-radius:0px',
            })
        }
    
    def __init__(self, hide_is_verified=True, hide_phone=True, *args, **kwargs):
        super(VerifiedRegisterForm, self).__init__(*args, **kwargs)
        self.fields['step'].widget = forms.HiddenInput()
        self.fields['step'].initial = 3 #step_number
        if hide_is_verified:
            self.fields['is_verified'].widget = forms.HiddenInput()
        if hide_phone:
            self.fields['phone'].widget = forms.HiddenInput()
    
    # check validation
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    
    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        try:
            phone_instance = phonenumbers.parse(phone, "BD")
            if not phonenumbers.is_possible_number(phone_instance):
                raise forms.ValidationError("Invalid phone number ")
                # (is_possible_number: False)
            if not phonenumbers.is_valid_number(phone_instance):
                raise forms.ValidationError("Invalid phone number ")
                # (is_possible_number: False)
        except phonenumbers.phonenumberutil.NumberParseException:
            raise forms.ValidationError("Invalid phone number")
        # print(phone_instance)
        # phone_as_e164 = phonenumbers.format_number(phone_instance, phonenumbers.PhoneNumberFormat.E164)
        return phone_instance

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = True
        if commit:
            user.save()
        return user


class PhoneVerifyForm(forms.Form):
    # phone = PhoneNumberField()
    phone = forms.CharField(label='')
    security_code = forms.CharField(label='', required=False)

    phone.widget.attrs.update({
        'placeholder': "Phone", 'title': 'Phone number (BD)'
    })
    security_code.widget.attrs.update({
        'placeholder': "Security code", 'title': 'Security code (OTP)', 'required': False,
    })

    # def __init__(self, request, *args, **kwargs):
    #     self.request = request
    #     super(PhoneVerifyForm, self).__init__(*args, **kwargs)

    # def clean(self):
    #     request = self.request
    #     data = self.cleaned_data
    #     phone = data.get("phone")
    #     security_code = data.get("security_code")
    #     try:
    #         phone_instance = phonenumbers.parse(phone, "BD")
    #         if not phonenumbers.is_possible_number(phone_instance):
    #             raise forms.ValidationError(
    #                 "Invalid phone number (is_possible_number: False)")
    #         if not phonenumbers.is_valid_number(phone_instance):
    #             raise forms.ValidationError(
    #                 "Invalid phone number (is_valid_number: False)")
    #     except phonenumbers.phonenumberutil.NumberParseException:
    #         raise forms.ValidationError("Invalid phone number")
    #     # print(phone_instance)

    #     print(f"phone:{phone}, security_code:{security_code}")
    #     return data
