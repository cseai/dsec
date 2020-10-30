from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.views.generic import CreateView, FormView, DetailView, View, UpdateView
from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404

import phonenumbers

# for phone verify
import requests
from phone_verify.models import SMSVerification
from accounts.sms_backends.utils import  check_verified_phone_number, delete_phone_smsverification_objects

from core.mixins import NextUrlMixin, RequestFormAttachMixin
from accounts.forms import LoginForm
from .forms import (
    RequsetRegisterForm, 
    OTPRegisterForm, 
    VerifiedRegisterForm,
    RequsetPasswordResetForm,
    OTPPasswordResetForm,
    VerifiedPasswordResetForm,
)

User = get_user_model()


class LoginView(NextUrlMixin, RequestFormAttachMixin, FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'auth/login.html'
    default_next = '/'

    def form_valid(self, form):
        next_path = self.get_next_url()
        return redirect(next_path)


def verify_then_redirect_register(request):
    """
    [PROBLEM]: When someone submitting (hitting multiple time very quickly) 
    for security code instantly program sending security code every time and
    then showing security code form.
    May be we can check last time security code send and to get again restrict in time constraints.
    """
    # step 1 for send security code
    # step 2 for verify security code
    current_step = 1 
    submit_btn_text = "Get Verification"

    if request.method =='POST':
        if 'security_code' in request.POST:
            form = OTPRegisterForm(request.POST or None, request.FILES or None)
            submit_btn_text = "Submit Verification"
            current_step = 2
        else:
            form = RequsetRegisterForm(request.POST or None, request.FILES or None)
        
        if form.is_valid():
            step_security_code = form.cleaned_data.get('security_code', None)
            
            if step_security_code:
                # security code validation was done in the form
                # but we also wanna check is it exist or not
                # check security_code and proced
                # Verify if security_code entered is correct
                # BUT KEEP IN MIND: our form's phone number may not str
                # we need to convert it to str
                # MAKE SURE phone_number IS STRING AS_E164 FORMAT (BD) i.e. +8801xxxxxxxxx
                if type(form.cleaned_data["phone"]) != str:
                    phone_number = phonenumbers.format_number(form.cleaned_data["phone"], phonenumbers.PhoneNumberFormat.E164)
                else:
                    phone_number = form.cleaned_data["phone"]
                security_code = form.cleaned_data["security_code"]

                smsv_instance = SMSVerification.objects.filter(
                    phone_number=phone_number,
                    security_code=security_code
                ).first()

                if smsv_instance and smsv_instance.is_verified:
                    # verify complete now redirect to register
                    session_token = smsv_instance.session_token
                    # register/<str:phone_number>/<str:security_code>/<str:session_token>
                    verify_and_register_url = f"/auth/register/{phone_number}/{security_code}/{session_token}/"
                    return redirect(verify_and_register_url)
                else:
                    # something went wrong 
                    # it should not enter this block
                    # because all verification confirmed in the form
                    # I am just passing it
                    # But if it happens we should debug what's going on in the form section
                    pass
            else:
                # that means security code was send or ignored
                # we just need to go to the next step
                # generate form for next step
                # MAKE SURE phone_number IS STRING AS_E164 FORMAT (BD) i.e. +8801xxxxxxxxx
                if type(form.cleaned_data["phone"]) != str:
                    phone_number = phonenumbers.format_number(form.cleaned_data["phone"], phonenumbers.PhoneNumberFormat.E164)
                else:
                    phone_number = form.cleaned_data["phone"]
                initial = {
                    "phone": phone_number
                }
                form = OTPRegisterForm(initial=initial)
                submit_btn_text = "Submit Verification"
                current_step = 2
    else:
        form = RequsetRegisterForm(request.POST or None, request.FILES or None)

    context = {
        'title': "Register (Verify Phone)",
        'main_heading': "register (Verify Phone)",
        'form': form,
        'current_step': current_step,
        'submit_btn_text': submit_btn_text,
    }
    return render(request, 'auth/verify_then_redirect_register.html', context)


def verify_and_register(request, phone_number, security_code, session_token, *args, **kwargs):
    # AT FIRST CHECK GIVEN phone_number, security_code, session_token ARE VALID
    # IF NOT, IT MEANS THE URL IS FAKE OR phone_verify EXPIRED OR DELETED
    is_verified_phone_number = check_verified_phone_number(phone_number, security_code, session_token)
    if not is_verified_phone_number:
        raise Http404("You are lost. Page does not exist")

    form = VerifiedRegisterForm(request.POST or None, initial={'phone': phone_number, 'is_verified': True})
    

    if form.is_valid():
        if is_verified_phone_number:
            # check user exist or not
            existed_user = User.objects.filter(phone=phone_number).first()
            if not existed_user:
                user = form.save(commit=False)
                # is_verified was set at form save() method
                # so we don't have to do it here
                user.save()
                #======BUGFIX=======
                # after register we must delete that SMSVerification object
                # so that user can not re-try using back-url
                succeed = delete_phone_smsverification_objects(phone_number=phone_number)
                if not succeed:
                    # something went wrong
                    pass
                else:
                    # succesfully removed
                    pass
                # now redirect to succed page or other page
                return redirect('/auth/login/')
            else:
                # that means somethig happend wrong or user exist
                # we just want to redirect 404 page
                raise Http404("You are lost. Page does not exist")
        else:
            # that means phone verification failed
            # it could be wrong or fake URL with 
            # /register/<str:phone_number>/<str:security_code>/<str:session_token>
            # or phone_verify wrong
            # we are just redirecting to 404 page
            raise Http404("You are lost. Page does not exist")

    context = {
        'title': "Verify and Register",
        'main_heading': "Register",
        'form': form,
        'submit_btn_text': "Submit",
    }
    return render(request, 'auth/verify_and_register.html', context)


def verify_then_redirect_password_reset(request):
    """
    [PROBLEM]: When someone submitting (hitting multiple time very quickly) 
    for security code instantly program sending security code every time and
    then showing security code form.
    May be we can check last time security code send and to get again restrict in time constraints.
    """
    # step 1 for send security code
    # step 2 for verify security code
    current_step = 1 
    submit_btn_text = "Get Verification"

    if request.method =='POST':
        if 'security_code' in request.POST:
            form = OTPPasswordResetForm(request.POST or None, request.FILES or None)
            submit_btn_text = "Submit Verification"
            current_step = 2
        else:
            form = RequsetPasswordResetForm(request.POST or None, request.FILES or None)

        if form.is_valid():
            step_security_code = form.cleaned_data.get('security_code', None)
            if step_security_code:
                # security code validation was done in the form
                # but we also wanna check is it exist or not
                # check security_code and proced
                # Verify if security_code entered is correct
                # MAKE SURE phone_number IS STRING AS_E164 FORMAT (BD) i.e. +8801xxxxxxxxx
                if type(form.cleaned_data["phone"]) != str:
                    phone_number = phonenumbers.format_number(form.cleaned_data["phone"], phonenumbers.PhoneNumberFormat.E164)
                else:
                    phone_number = form.cleaned_data["phone"]
                security_code = form.cleaned_data["security_code"]

                smsv_instance = SMSVerification.objects.filter(
                    phone_number=phone_number,
                    security_code=security_code
                ).first()

                if smsv_instance and smsv_instance.is_verified:
                    # verify complete now redirect to password_reset
                    session_token = smsv_instance.session_token
                    # password-reset/<str:phone_number>/<str:security_code>/<str:session_token>
                    verify_and_password_reset_url = f"/auth/password-reset/{phone_number}/{security_code}/{session_token}/"
                    return redirect(verify_and_password_reset_url)
                else:
                    # something went wrong 
                    # it should not enter this block
                    # because all verification confirmed in the form
                    # I am just passing it
                    # But if it happens we should debug what's going on in the form section
                    pass
            else:                
                # that means security code was send or ignored
                # we just need to go to the next step
                # generate form for next step
                # MAKE SURE phone_number IS STRING AS_E164 FORMAT (BD) i.e. +8801xxxxxxxxx
                if type(form.cleaned_data["phone"]) != str:
                    phone_number = phonenumbers.format_number(form.cleaned_data["phone"], phonenumbers.PhoneNumberFormat.E164)
                else:
                    phone_number = form.cleaned_data["phone"]
                initial = {
                    "phone": phone_number
                }
                form = OTPPasswordResetForm(initial=initial)
                submit_btn_text = "Submit Verification"
                current_step = 2
    else:
        form = RequsetPasswordResetForm(request.POST or None, request.FILES or None)

    context = {
        'title': "Passward Reset",
        'main_heading': "Passward Reset",
        'form': form,
        'current_step': current_step,
        'submit_btn_text': submit_btn_text,
    }
    return render(request, 'auth/verify_then_redirect_password_reset.html', context)


def verify_and_password_reset(request, phone_number, security_code, session_token, *args, **kwargs):
    # AT FIRST CHECK GIVEN phone_number, security_code, session_token ARE VALID
    # IF NOT, IT MEANS THE URL IS FAKE OR phone_verify EXPIRED OR DELETED
    is_verified_phone_number = check_verified_phone_number(phone_number, security_code, session_token)
    if not is_verified_phone_number:
        raise Http404("You are lost. Page does not exist")

    form = VerifiedPasswordResetForm(request.POST or None, initial={'phone': phone_number})
    
    if form.is_valid():
        if is_verified_phone_number:
            # check user exist or not
            existed_user = User.objects.filter(phone=phone_number).first()
            if existed_user:
                # user exist 
                # so we are ready to reset password
                new_password = form.cleaned_data.get('password1')
                existed_user.set_password(new_password)
                # save changes to database by calling save() method
                existed_user.save()
                #======BUGFIX=======
                # after passward reset we must delete that SMSVerification object
                # so that user can not re-try using back-url
                succeed = delete_phone_smsverification_objects(phone_number=phone_number)
                if not succeed:
                    # something went wrong
                    pass
                else:
                    # succesfully removed
                    pass
                # now redirect to password reset succed page
                return redirect('/auth/password-reset/done/')
            else:
                # that means somethig happend wrong or user deleted
                # we just want to redirect password reset failed page
                return redirect('/auth/password-reset/failed/')
        else:
            # that means phone verification failed
            # it could be wrong or fake URL with 
            # /password-reset/<str:phone_number>/<str:security_code>/<str:session_token>
            # or phone_verify wrong
            # we are just redirecting to 404 page
            raise Http404("You are lost. Page does not exist")

    context = {
        'title': "Password Reset",
        'main_heading': "Password Reset",
        'form': form,
        'submit_btn_text': "Submit",
    }
    return render(request, 'auth/verify_and_password_reset.html', context)


def password_reset_done(request):
    password_reset_done_message = "Password reset success. Now you can login with your new password!"
    context = {
        'title': "Password Reset Done",
        'main_heading': "Password Reset Done",
        'password_reset_done_message': password_reset_done_message,
    }
    return render(request, 'auth/password_reset_done.html', context)


def password_reset_failed(request):
    password_reset_failed_message = "Password reset failed. Please check everything right then try again!"
    context = {
        'title': "Password Reset Failed",
        'main_heading': "Password Reset Failed",
        'password_reset_failed_message': password_reset_failed_message,
    }
    return render(request, 'auth/password_reset_failed.html', context)