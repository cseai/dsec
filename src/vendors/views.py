from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import RegisterStoreForm

@login_required
def register_vendor_store_view(request, *args, **kwargs):
    form = RegisterStoreForm(request.POST or None, request.FILES or None)
    if request.method =='POST':
        if form.is_valid():
            # process the data in form.cleaned_data as required
            print(form.cleaned_data)
            return HttpResponseRedirect('/')
    context = {
        'form': form,
    }
    return render(request, 'register_vendor_store.html', context)

