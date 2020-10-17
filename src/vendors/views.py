from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import RegisterStoreForm

from vendors.models import Store
from addresses.models import Address

@login_required
def register_vendor_store_view(request, *args, **kwargs):
    form = RegisterStoreForm(request.POST or None, request.FILES or None)
    if request.method =='POST':
        if form.is_valid():
            # process the data in form.cleaned_data as required
            title = form.cleaned_data.get('title')
            category = form.cleaned_data.get('category')
            opening_time = form.cleaned_data.get('opening_time')
            closing_time = form.cleaned_data.get('closing_time')
            
            # address info
            address_line_1 = form.cleaned_data.get('address_line_1')
            address_line_2 = form.cleaned_data.get('address_line_2')
            city = form.cleaned_data.get('city')
            state = form.cleaned_data.get('state')
            postal_code = form.cleaned_data.get('postal_code')
            country = form.cleaned_data.get('country')

            # create address instance
            try:
                address = Address.objects.create(
                    address_type='parmanent',
                    line_1=address_line_1,
                    line_2=address_line_2,
                    city=city,
                    state=state,
                    postal_code=postal_code,
                    country=country
                )
            except:
                raise forms.ValidationError("Invalid Address Information!")
            
            # create store instance
            try:
                store = Store.objects.create(
                    title=title,
                    user=request.user,
                    category=category,
                    opening_time=opening_time,
                    closing_time=closing_time,
                    address=address
                )
            except:
                raise forms.ValidationError("Invalid Store Information!")
            
            return HttpResponseRedirect('/')
    context = {
        'form': form,
    }
    return render(request, 'vendors/register_vendor_store.html', context)

