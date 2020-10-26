from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

# forms
from accounts.forms import UserUpdateForm
from addresses.forms import AddressUpdateForm
from .forms import ProfileUpdateForm

from .models import Profile

@login_required
def user_profile_home_view(request):
    context = {
        'user': request.user,
        'title':'Profile'
    }
    return render(request, 'profiles/user_profile_home.html', context)

@login_required
def user_profile_update_view(request):
    user_instance = request.user
    try:
        # profile_instance = user_instance.profile
        _ = user_instance.profile
    except:
        user_instance.profile = Profile.objects.create(user=user_instance)
        user_instance.save()
    
    # all forms
    user_form = UserUpdateForm(request.POST or None, request.FILES or None, instance=user_instance)
    profile_form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=user_instance.profile)
    address_form = AddressUpdateForm(request.POST or None, request.FILES or None, instance=user_instance.profile.address)
    
    if request.method =='POST':
        if user_form.is_valid() and profile_form.is_valid() and address_form.is_valid():
            user_profile = profile_form.save(commit=False)
            profile_address = address_form.save()
            if profile_address:
                user_profile.address = profile_address
            user_profile.save()
            user = user_form.save(commit=False)
            if user_profile:
                user.profile = user_profile
            user.save()
            return HttpResponseRedirect('/profile/')
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'address_form': address_form,
        'title': 'Profile Update',
        'form_heading': "Profile Update",
    }
    return render(request, 'profiles/user_profile_update.html', context)
