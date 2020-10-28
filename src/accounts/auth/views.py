from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, FormView, DetailView, View, UpdateView
from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpResponseRedirect

import phonenumbers

# for phone verify
import requests
from phone_verify.models import SMSVerification
from accounts.sms_backends.utils import  check_verified_phone_number

from core.mixins import NextUrlMixin, RequestFormAttachMixin
from accounts.forms import LoginForm, RegisterForm
from .forms import (
    PhoneVerifyForm, 
    RequsetRegisterForm, 
    OTPRegisterForm, 
    VerifiedRegisterForm,
)

class LoginView(NextUrlMixin, RequestFormAttachMixin, FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'auth/login.html'
    default_next = '/'

    def form_valid(self, form):
        next_path = self.get_next_url()
        return redirect(next_path)


def verify_and_register(request, phone_number, security_code, session_token, *args, **kwargs):
    # print("params:", phone_number, security_code)
    form = RegisterForm(request.POST or None, initial={'phone': phone_number})
    # print(f"post-data[{request.method}]:{form.data}, POST={request.POST}")
    if form.is_valid():
        is_verified_phone_number = check_verified_phone_number(phone_number, security_code, session_token)
        if is_verified_phone_number:
            user = form.save(commit=False)
            user.is_verified = True
            user.save()
            # print(f"user:{user}")
            return redirect('/auth/login/')
        else:
            return HttpResponseRedirect('/auth/register/')
    context = {
        'form': form,
    }
    return render(request, 'auth/verify_and_register.html', context)


def verify_then_redirect_register(request):
    """
    [PROBLEM]: When someone submitting (hitting multiple time very quickly) 
    for security code instantly program sending security code every time and
    then showing security code form.
    May be we can check last time security code send and to get again restrict in time constraints.
    """
    submit_btn_text = "Get Verification"
    if request.method =='POST':
        if 'security_code' in request.POST:
            form = OTPRegisterForm(request.POST or None, request.FILES or None)
            submit_btn_text = "Submit Verification"
            # print(f"security_code=>form.is_valid()={form.is_valid()}, data={form.data}")
        else:
            form = RequsetRegisterForm(request.POST or None, request.FILES or None)
            # print(f"else=>form.is_valid()={form.is_valid()}, data={form.data}")
        if form.is_valid():
            # print(f"form.cleaned_data={form.cleaned_data}")
            step_security_code = form.cleaned_data.get('security_code', None)
            # print(f"step_security_code:{step_security_code}")
            if step_security_code:
                # check security_code and proced
                # Verify if security_code entered is correct
                # POST /api/phone/verify
                phone_number = form.cleaned_data["phone"]
                security_code = form.cleaned_data["security_code"]

                smsv_instance = SMSVerification.objects.filter(
                    phone_number=phone_number,
                    security_code=security_code
                ).first()

                # print(f"phone:{phone_number}")
                # print(f"smsv_instance:{smsv_instance}")
                if smsv_instance and smsv_instance.is_verified == False:
                    # ready to verify then redirect to register
                    session_token = smsv_instance.session_token
                    data = {
                        "phone_number": phone_number,
                        "security_code": security_code,
                        "session_token": smsv_instance.session_token,
                    }
                    # print(f"host:{request.get_host()}")
                    base_url = 'http://127.0.0.1:8000'
                    url_for_phone_verify = f"{base_url}/api/phone-verify/phone/verify"
                    response = requests.post(url=url_for_phone_verify, data=data)
                    # print(f'response(verify): status={response.status_code}, text={response.text}')

                    if response.status_code == 200:
                        # verify complete now redirect to register
                        base_url = 'http://127.0.0.1:8000'
                        # verify-register/<str:phone_number>/<int:security_code>/<str:session_token>
                        verify_and_register_url = f"/auth/register/{phone_number}/{security_code}/{session_token}/"
                        # return HttpResponseRedirect(verify_and_register_url)
                        # return redirect('verify_and_register', args=(phone_number, security_code,session_token))
                        return redirect(verify_and_register_url)
                    else:
                        # security_code expired or something happend
                        # handle this by showing message
                        print("Invalid security code!")
                elif smsv_instance and smsv_instance.is_verified:
                    # already verified phone_number
                    # it can be different situation
                    # handle this by showing message
                    print("Invalid security code!")
                else:
                    # wrong phone number or security code
                    # handle this by showing message
                    print("WRONG phone or security code")
            else:
                # Send security_code on given phone_number
                # POST /api/phone-verify/phone/register
                if type(form.cleaned_data["phone"]) != str:
                    phone_number = phonenumbers.format_number(form.cleaned_data["phone"], phonenumbers.PhoneNumberFormat.E164)
                else:
                    phone_number = form.cleaned_data["phone"]
                data = {
                    "phone_number": phone_number, #form.cleaned_data["phone"]
                }
                base_url = 'http://127.0.0.1:8000'
                url = f"{base_url}/api/phone-verify/phone/register"
                response = requests.post(url=url, data=data)
                # print(f'response(send):{response}')
                # print(f'response(send)-status:{response.status_code}')
                # print(f'response(send)-data:{response.text}')

                # generate form for next step
                if response.status_code == 200:
                    initial = {
                        "phone": form.cleaned_data["phone"]
                    }
                    # form = OTPRegisterForm(request.POST or None, request.FILES or None, initial=initial)
                    form = OTPRegisterForm(initial=initial)
                    submit_btn_text = "Submit Verification"
        # else:
        #     print(f"Errors:{form.errors}")
    else:
        form = RequsetRegisterForm(request.POST or None, request.FILES or None)

    # print(f"data:{form.data}")
    context = {
        'form': form,
        'submit_btn_text': submit_btn_text,
    }
    return render(request, 'auth/verify_then_register.html', context)