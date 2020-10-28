from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, FormView, DetailView, View, UpdateView
from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpResponseRedirect

import phonenumbers

# for phone verify
import requests
from phone_verify.models import SMSVerification


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


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'auth/register.html'
    success_url = '/auth/login/'

def verify_and_register(request, phone_number, security_code, session_token):
    print("params:", phone_number, security_code)
    def check_verified_phone_number(phone_number, security_code, session_token):
        smsv_instance = SMSVerification.objects.filter(
            phone_number=phone_number,
            security_code=security_code,
            session_token=session_token,
            is_verified=True
        ).first()
        if smsv_instance:
            return True
        else:
            False
    
    is_verified_phone_number = check_verified_phone_number(phone_number, security_code, session_token)
    
    if is_verified_phone_number:
        data = {
            "phone": phone_number,
            "is_verified": is_verified_phone_number,
        }
        form = RegisterForm(request.POST or None, request.FILES or None)
        if request.method == "GET":
            form = RegisterForm(initial=data)
            print(f"get-data:{form.data}")
        if request.method == "POST":
            form = RegisterForm(request.POST or None, request.FILES or None)
            print(f"post-data:{form.data}, POST={request.POST}")
            if form.is_valid():
                user = form.save()
                print(f"user:{user}")
                return redirect('/auth/login/')
            else:
                print(f"form={form.data}")
        context = {
            'form': form,
        }
        return render(request, 'auth/verify_and_register.html', context)
    else:
        return HttpResponseRedirect('/auth/verify-register/')



def verify_then_redirect_register(request):
    submit_btn_text = "Get Verification"
    if request.method =='POST':
        if 'security_code' in request.POST:
            form = OTPRegisterForm(request.POST or None, request.FILES or None)
            submit_btn_text = "Submit Verification"
            print(f"security_code=>form.is_valid()={form.is_valid()}, data={form.data}")
        else:
            form = RequsetRegisterForm(request.POST or None, request.FILES or None)
            print(f"else=>form.is_valid()={form.is_valid()}, data={form.data}")
        if form.is_valid():
            print(f"form.cleaned_data={form.cleaned_data}")
            step_security_code = form.cleaned_data.get('security_code', None)
            print(f"step_security_code:{step_security_code}")
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

                print(f"phone:{phone_number}")
                print(f"smsv_instance:{smsv_instance}")
                if smsv_instance and smsv_instance.is_verified == False:
                    # ready to verify then redirect to register
                    session_token = smsv_instance.session_token
                    data = {
                        "phone_number": phone_number,
                        "security_code": security_code,
                        "session_token": smsv_instance.session_token,
                    }
                    print(f"host:{request.get_host()}")
                    base_url = 'http://127.0.0.1:8000'
                    url_for_phone_verify = f"{base_url}/api/phone-verify/phone/verify"
                    response = requests.post(url=url_for_phone_verify, data=data)
                    print(f'response(verify): status={response.status_code}, text={response.text}')

                    if response.status_code == 200:
                        # verify complete now redirect to register
                        base_url = 'http://127.0.0.1:8000'
                        # verify-register/<str:phone_number>/<int:security_code>/<str:session_token>
                        verify_and_register_url = f"auth/verify-register/{phone_number}/{security_code}/{session_token}/"
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
                print(f'response(send):{response}')
                print(f'response(send)-status:{response.status_code}')
                print(f'response(send)-data:{response.text}')

                # generate form for next step
                if response.status_code == 200:
                    initial = {
                        "phone": form.cleaned_data["phone"]
                    }
                    # form = OTPRegisterForm(request.POST or None, request.FILES or None, initial=initial)
                    form = OTPRegisterForm(initial=initial)
                    submit_btn_text = "Submit Verification"
        else:
            print(f"Errors:{form.errors}")
    else:
        form = RequsetRegisterForm(request.POST or None, request.FILES or None)

    print(f"data:{form.data}")
    context = {
        'form': form,
        'submit_btn_text': submit_btn_text,
    }
    return render(request, 'auth/verify_then_register.html', context)

def verify_then_register_hacked(request):
    # step = 1 for getting phone number
    # step = 2 for verifing phone number
    # step = 3 for register
    if request.method == 'GET':   
        step = 1
        form = RequsetRegisterForm(request.POST or None, request.FILES or None)
    elif request.method == 'POST':
        print(f"POST-data={request.POST}")
        if 'step' in request.POST:
            step = int(request.POST['step'])
            print(f"step:{step}, type:{type(step)}")
        else:
            step = None
        if step == 1:
            form = RequsetRegisterForm(request.POST or None, request.FILES or None)
            print(f"step:{step}, form-data:{form.data}")
            if form.is_valid():
                # Send security_code on given phone_number
                # POST /api/phone-verify/phone/register
                data = {
                    "phone_number": form.cleaned_data["phone"]
                }
                base_url = 'http://127.0.0.1:8000'
                url = f"{base_url}/api/phone-verify/phone/register"
                response = requests.post(url=url, data=data)
                print(f'response(send):{response}')
                print(f'response(send)-status:{response.status_code}')
                print(f'response(send)-data:{response.text}')

                # generate form for next step
                if response.status_code == 200:
                    initial = {
                        "phone": form.cleaned_data["phone"],
                        "security_code": '',
                    }
                    # form = OTPRegisterForm(request.POST or None, request.FILES or None, initial=initial)
                    form = OTPRegisterForm(initial=initial)
                    # update step: step = 2
                    step = 2

        elif step == 2:
            form = OTPRegisterForm(request.POST or None, request.FILES or None)
            print(f"step:{step}, form-data:{form.data}")
            if form.is_valid():
                # check security_code and proced
                # Verify if security_code entered is correct
                # POST /api/phone/verify
                obj = SMSVerification.objects.filter(
                    phone_number=form.cleaned_data["phone"]
                ).first()
                obj_list = SMSVerification.objects.all()
                if obj == None:
                    obj = obj_list[0]
                # print(f"obj:{obj}, phone:{obj.phone_number}, security_code:{obj.security_code}, session_token:{obj.session_token}")
                print(f"obj:{obj}")
                data = {
                    "phone_number": form.cleaned_data["phone"], #obj.phone_number.as_e164, #form.cleaned_data["phone"],
                    "security_code": form.cleaned_data["security_code"],
                    "session_token": obj.session_token #"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrODgwMTc4MzY0NTUyOCIsIm5vbmNlIjowLjU1Mjg5Mjk1ODI2MzkyMTR9.tn9XmHV4HFjhg10XJw2HjEQR",
                }
                base_url = 'http://127.0.0.1:8000'
                url = f"{base_url}/api/phone-verify/phone/verify"
                response = requests.post(url=url, data=data)
                print(f'response(verify):{response}')
                print(f'response(verify)-status:{response.status_code}')
                print(f'response(verify)-text:{response.text}')

                # generate form for next step
                if  response.status_code == 200:
                    initial = {
                        "phone": form.cleaned_data["phone"],
                        "is_verified": True,
                    }
                    # form = VerifiedRegisterForm(request.POST or None, request.FILES or None, initial=initial)
                    form = VerifiedRegisterForm(initial=initial)
                    # update step: step = 3
                    step = 3
                else:
                    print("INVALID security_code!!!")
                    # initial = {
                    #     "phone": form.cleaned_data["phone"],
                    # }
                    # # form = OTPRegisterForm(request.POST or None, request.FILES or None, initial=initial)
                    # form = OTPRegisterForm(initial=initial)
        elif step == 3:
            form = VerifiedRegisterForm(request.POST or None, request.FILES or None)
            print(f"step:{step}, form-data:{form.data}, form:{form}")
            if form.is_valid():
                # verification completed and now ready to register
                user = form.save()
                print(f"user:{user}")
                return HttpResponseRedirect('/auth/login/')
            
        else:
            print("INVALID STEP")
            form = None
            step = None
    else:
        # NOT A VALID REQUEST METHOD [GET,POST]
        form = None
        step = None
        print(f"INVALID REQUEST.METHOD")
    # print(f"data:{form.data}")
    context = {
        'step': step,
        'form': form,
    }
    return render(request, 'auth/verify_then_register.html', context)



def verify_then_register_old(request):
    print(f"session: {request.session.keys()}")
    if request.session.get('test', None):
        print(f"session-test: {request.session.keys()}")
    else:
        request.session['test'] = "Test"
        print("session setted")

    # form = RequsetRegisterForm(request.POST or None, request.FILES or None)
    print(f"request.POST:{request.POST}")
    print(f"request.POST.items():{request.POST.items()}")
    if request.method =='POST':
        data = { key: value for key, value in request.POST.items()}
        try:
            del data['csrfmiddlewaretoken']
        except:
            pass
        print(f"post-data:{data}")
        print(f"security_code:{ 'security_code' in request.POST}")
        print(f"password1:{ 'password1' in request.POST }")
        if 'security_code' in request.POST:
            form = OTPRegisterForm(request.POST or None, request.FILES or None)
            print(f"security_code=>form.is_valid()={form.is_valid()}, data={form.data}")
        elif 'password1' in request.POST:
            # form = VerifiedRegisterForm(request.POST or None, request.FILES or None)
            # form = VerifiedRegisterForm(data)
            form = RegisterForm(request.POST or None, request.FILES or None)
            print(f"password1=>form.is_valid()={form.is_valid()}, data={form.data}")
        else:
            
            form = RequsetRegisterForm(request.POST or None, request.FILES or None)
            print(f"else=>form.is_valid()={form.is_valid()}, data={form.data}")
        if form.is_valid():
            print(f"form.cleaned_data={form.cleaned_data}")
            step_security_code = form.cleaned_data.get('security_code', None)
            step_verified_and_register = form.cleaned_data.get('is_verified', None)
            print(f"step_security_code:{step_security_code}\nstep_verified_and_register:{step_verified_and_register}")
            if step_security_code:
                # check security_code and proced
                # Verify if security_code entered is correct
                # POST /api/phone/verify
                obj = SMSVerification.objects.filter(
                    phone_number=form.cleaned_data["phone"]
                ).first()
                obj_list = SMSVerification.objects.all()
                if obj == None:
                    obj = obj_list[0]
                # print(f"obj:{obj}, phone:{obj.phone_number}, security_code:{obj.security_code}, session_token:{obj.session_token}")
                print(f"obj:{obj}")
                data = {
                    "phone_number": form.cleaned_data["phone"], #obj.phone_number.as_e164, #form.cleaned_data["phone"],
                    "security_code": form.cleaned_data["security_code"],
                    "session_token": obj.session_token #"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrODgwMTc4MzY0NTUyOCIsIm5vbmNlIjowLjU1Mjg5Mjk1ODI2MzkyMTR9.tn9XmHV4HFjhg10XJw2HjEQR",
                }
                base_url = 'http://127.0.0.1:8000'
                url = f"{base_url}/api/phone-verify/phone/verify"
                response = requests.post(url=url, data=data)
                print(f'response(verify):{response}')
                print(f'response(verify)-status:{response.status_code}')
                print(f'response(verify)-text:{response.text}')

                # generate form for next step
                if  response.status_code == 200:
                    if type(form.cleaned_data["phone"]) != str:
                        phone_number = phonenumbers.format_number(form.cleaned_data["phone"], phonenumbers.PhoneNumberFormat.E164)
                    else:
                        phone_number = form.cleaned_data["phone"]
                    phone_instance = phonenumbers.parse(phone_number, "BD")
                    initial = {
                        "phone": phone_instance, #form.cleaned_data["phone"],
                        "is_verified": True,
                    }
                    # form = VerifiedRegisterForm(request.POST or None, request.FILES or None, initial=initial)
                    # form = VerifiedRegisterForm(initial=initial)
                    form = RegisterForm(initial=initial)
                else:
                    print("INVALID security_code!!!")
                    initial = {
                        "phone": form.cleaned_data["phone"],
                    }
                    # form = OTPRegisterForm(request.POST or None, request.FILES or None, initial=initial)
                    form = OTPRegisterForm(initial=initial)

            elif step_verified_and_register:
                # verification completed and now ready to register
                user = form.save()
                print(f"user:{user}")
                return HttpResponseRedirect('/auth/login/')
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
                print(f'response(send):{response}')
                print(f'response(send)-status:{response.status_code}')
                print(f'response(send)-data:{response.text}')

                # generate form for next step
                if response.status_code == 200:
                    initial = {
                        "phone": form.cleaned_data["phone"],
                        "security_code": '',
                    }
                    # form = OTPRegisterForm(request.POST or None, request.FILES or None, initial=initial)
                    form = OTPRegisterForm(initial=initial)
        else:
            print(f"Errors:{form.errors}")
    else:
        form = RequsetRegisterForm(request.POST or None, request.FILES or None)

    print(f"data:{form.data}")
    context = {
        'form': form,
    }
    return render(request, 'auth/verify_then_register.html', context)


def show_phone_verification_table(request):
    obj_list = SMSVerification.objects.all()
    context = {
        'obj_list': obj_list,
    }
    return render(request, 'auth/show_phone_verification_table.html', context)


# phone verification
def verify_phone(request):
    form = PhoneVerifyForm(request.POST or None, request.FILES or None)
    if request.method =='POST':
        # print(f"cleaned_data:{form.cleaned_data}")
        if form.is_valid():
            print(f"data:{form.cleaned_data}")
            if form.cleaned_data["security_code"] == "":
                # Send security_code on given phone_number
                # POST /api/phone/register
                data = {
                    "phone_number": '+8801783645528' #str(form.cleaned_data["phone"]),
                }
                base_url = 'http://127.0.0.1:8000'
                url = f"{base_url}/api/phone-verify/phone/register"
                response = requests.post(url=url, data=data)
                # response = requests.post(url="http://google.com", data=data)
                print(f'response(send):{response}')
                print(f'response(send)-status:{response.status_code}')
                print(f'response(send)-data:{response.text}')
                res = requests.get(url=base_url)
                print(res.status_code)
            else:
                # Verify if security_code entered is correct
                # POST /api/phone/verify
                obj = SMSVerification.objects.filter(
                    phone_number=form.cleaned_data["phone"]
                ).first()
                obj_list = SMSVerification.objects.all()
                if obj == None:
                    obj = obj_list[0]
                # print(f"obj:{obj}, phone:{obj.phone_number}, security_code:{obj.security_code}, session_token:{obj.session_token}")
                print(f"obj:{obj}")
                data = {
                    "phone_number": obj.phone_number.as_e164, #form.cleaned_data["phone"],
                    "security_code": form.cleaned_data["security_code"],
                    "session_token": obj.session_token #"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrODgwMTc4MzY0NTUyOCIsIm5vbmNlIjowLjU1Mjg5Mjk1ODI2MzkyMTR9.tn9XmHV4HFjhg10XJw2HjEQR",
                }
                base_url = 'http://127.0.0.1:8000'
                url = f"{base_url}/api/phone-verify/phone/verify"
                response = requests.post(url=url, data=data)
                print(f'response(verify):{response}')
                print(f'response(verify)-status:{response.status_code}')
                print(f'response(verify)-text:{response.text}')
            # return HttpResponseRedirect('/')
        print(f"data-post:{form.data}")
    print(f"data:{form.data}")
    context = {
        'form': form,
    }
    return render(request, 'auth/verify_phone.html', context)