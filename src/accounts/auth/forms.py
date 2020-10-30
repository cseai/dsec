from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from phonenumber_field.formfields import PhoneNumberField
import phonenumbers

# for phone verify
import requests
from phone_verify.models import SMSVerification
from accounts.sms_backends.utils import  (
    check_verified_phone_number,
    phone_verify_register,
    phone_verify_verify,
)

User = get_user_model()


class RequsetRegisterForm(forms.Form):
    phone = forms.CharField(label='')
    
    phone.widget.attrs.update({
        'placeholder': "Phone", 'title': 'Phone number (BD)'
    })

    def __init__(self, *args, **kwargs):
        super(RequsetRegisterForm, self).__init__(*args, **kwargs)

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

        # check is it (account of this phone) already exist or not
        # do it at clean() method
        # existed_user = User.objects.filter(phone=phone_instance).first()
        # if existed_user:
        #     raise forms.ValidationError("Account already exist! Try another phone or login.")

        return phone_as_e164

    
    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get('phone')

        if phone:
            # check account of this phone is exist or not
            # we will not send security code to that number if account already exist
            existed_user = User.objects.filter(phone=phone).first()
            if existed_user:
                # so we have to raise phone validation error
                self.add_error('phone', ValidationError("Account already exist! Try another phone or login."))
                # raise forms.ValidationError("Account already exist! Try another phone or login.")
            else:
                # Send security_code on given phone_number
                # Use utils function
                # MAKE SURE phone_number IS STRING AS_E164 FORMAT (BD) i.e. +8801xxxxxxxxx
                if type(phone) != str:
                    phone_number = phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.E164)
                else:
                    phone_number = phone
                data = {
                    "phone_number": phone_number,
                }
                response, succeed = phone_verify_register(data=data)

                if succeed:
                    # that means message sent success
                    pass
                else:
                    # somthing went wrong with sending OTP or phone_verify
                    raise ValidationError("Something went wrong! Please try agin later.")


class OTPRegisterForm(forms.Form):
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
    

    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get('phone')
        security_code = cleaned_data.get('security_code')

        if phone and security_code:
            # check this phone is exist or not
            # check if phone exist then security_code valid or not
            # in both case raise corresponding validation error

            # we will raise validation error if user exist 
            # otherwise verify security_code
            existed_user = User.objects.filter(phone=phone).first()
            if existed_user:
                # that means user already exist 
                # set validation error
                self.add_error('phone', ValidationError("Account already exist! Try another phone or login."))
            else:
                # check security_code valid or not
                # MAKE SURE phone_number IS STRING AS_E164 FORMAT (BD) i.e. +8801xxxxxxxxx
                if type(phone) != str:
                    phone_number = phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.E164)
                else:
                    phone_number = phone

                smsv_instance = SMSVerification.objects.filter(
                    phone_number=phone_number,
                    security_code=security_code
                ).first()

                if smsv_instance and smsv_instance.is_verified == False:
                    # ready to verify then redirect to register
                    # Verify security_code on given phone_number, security_code and session_token 
                    # Use utils function
                    # MAKE SURE phone_number IS STRING AS_E164 FORMAT (BD) i.e. +8801xxxxxxxxx
                    session_token = smsv_instance.session_token
                    data = {
                        "phone_number": phone_number,
                        "security_code": security_code,
                        "session_token": session_token,
                    }
                    response, succeed = phone_verify_verify(data=data)

                    if succeed:
                        # that means verify succeed
                        pass
                    else:
                        # security_code expired or something happend
                        # handle this by showing message
                        self.add_error('security_code', ValidationError("Invalid Security Code!"))
                else:
                    self.add_error('security_code', ValidationError("Invalid Security Code!"))


class VerifiedRegisterForm(forms.ModelForm):
    """A form for creating new users after phone verification. Includes all the required
    fields, plus a repeated password."""
    # phone must be disabled for the case of phone verification
    phone = forms.CharField(label='', disabled=True)
    is_verified = forms.BooleanField(label='Verified', initial=True, disabled=True)
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={
        'placeholder': "Password"
    }))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={
        'placeholder': "Password confirmation"
    }))

    phone.widget.attrs.update({
        'placeholder': "Phone", 'title': 'Phone number (BD)'
    })

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'gender', 'email', 'phone', 'is_verified',)
        # customize form attrs
        labels = {
            'first_name': '',
            'last_name': '',
            'email': '',
            'gender': '',
            'is_verified': '',
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
            }),
            # 'is_verified': forms.BooleanField(attrs={
            #     'placeholder': "Verified",
            #     'required': True,
            #     'disabled': True,
            # })
        }

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
        # check is it (account of this phone) already exist or not
        # probably this field is uneditable but we will check it
        existed_user = User.objects.filter(phone=phone_instance).first()
        if existed_user:
            raise forms.ValidationError("Invalid phone. Account already exist!")

        # in this case we will return phonenumbers phone_instance
        # because it will store in databse as an phone_instance
        # but if we want to use this phone_instance in views then 
        # we need to convert it as str (phone_as_e164)
        return phone_instance

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(VerifiedRegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = True
        # set is_verified = True because user already verified
        user.is_verified = True
        if commit:
            user.save()
        return user


class RequsetPasswordResetForm(forms.Form):
    phone = forms.CharField(label='')
    
    phone.widget.attrs.update({
        'placeholder': "Phone", 'title': 'Phone number (BD)'
    })

    def __init__(self, *args, **kwargs):
        super(RequsetPasswordResetForm, self).__init__(*args, **kwargs)

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

        # check is it (account of this phone) already exist or not
        # we will ignore this validation becuse it can couse a attact
        # existed_user = User.objects.filter(phone=phone_instance).first()
        # if not existed_user:
        #     raise forms.ValidationError("Account does not exist! Please register first!")

        return phone_as_e164
    

    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get('phone')

        if phone:
            # check account of this phone is exist or not
            # we will ignore this validation becuse it can couse a attact
            # we just do not send security code to that number
            existed_user = User.objects.filter(phone=phone).first()
            if existed_user:
                # Send security_code on given phone_number
                # Use utils function
                # MAKE SURE phone_number IS STRING AS_E164 FORMAT (BD) i.e. +8801xxxxxxxxx
                if type(phone) != str:
                    phone_number = phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.E164)
                else:
                    phone_number = phone
                data = {
                    "phone_number": phone_number,
                }
                response, succeed = phone_verify_register(data=data)

                if succeed:
                    # that means message sent success
                    pass
                else:
                    # somthing went wrong with sending OTP or phone_verify
                    raise ValidationError("Something went wrong! Please try agin later.")
            else:
                # just ignore
                pass


class OTPPasswordResetForm(forms.Form):
    phone = forms.CharField(label='')
    security_code = forms.CharField(label='', required=True)

    phone.widget.attrs.update({
        'placeholder': "Phone", 'title': 'Phone number (BD)'
    })
    security_code.widget.attrs.update({
        'placeholder': "Security code", 'title': 'Security code (OTP)',
    })

    def __init__(self, *args, **kwargs):
        super(OTPPasswordResetForm, self).__init__(*args, **kwargs)
    
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
    

    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get('phone')
        security_code = cleaned_data.get('security_code')

        if phone and security_code:
            # check this phone is exist or not
            # check if phone exist then security_code valid or not
            # in both case raise only "Invalid Security Code!" message for security reason

            # we will ignore this validation becuse it can couse a attact
            existed_user = User.objects.filter(phone=phone).first()
            if not existed_user:
                self.add_error('security_code', ValidationError("Invalid Security Code!"))
            else:
                # check security_code valid or not
                phone_number = phone # must be string like +8801xxxxxxxxx

                smsv_instance = SMSVerification.objects.filter(
                    phone_number=phone_number,
                    security_code=security_code
                ).first()

                if smsv_instance and smsv_instance.is_verified == False:
                    # ready to verify then redirect to password_reset
                    session_token = smsv_instance.session_token
                    data = {
                        "phone_number": phone_number,
                        "security_code": security_code,
                        "session_token": smsv_instance.session_token,
                    }
                    response, succeed = phone_verify_verify(data=data)

                    if succeed:
                        # that means verify succeed
                        pass
                    else:
                        # security_code expired or something happend
                        # handle this by showing message
                        self.add_error('security_code', ValidationError("Invalid Security Code!"))
                else:
                    self.add_error('security_code', ValidationError("Invalid Security Code!"))


class VerifiedPasswordResetForm(forms.Form):
    """A form to reset password of an existed and verified user."""
    # phone must be disabled for the case of phone verification
    phone = forms.CharField(label='', disabled=True)
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={
        'placeholder': "New Password"
    }))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={
        'placeholder': "Password confirmation"
    }))

    phone.widget.attrs.update({
        'placeholder': "Phone", 'title': 'Phone number (BD)'
    })


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
        # check is it (account of this phone) already exist or not
        # probably this field is uneditable but we will check it
        existed_user = User.objects.filter(phone=phone_instance).first()
        if not existed_user:
            raise forms.ValidationError("Invalid phone number!")
        phone_as_e164 = phonenumbers.format_number(phone_instance, phonenumbers.PhoneNumberFormat.E164)
        # return phone_instance
        return phone_as_e164
