from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render, reverse, get_object_or_404
from django import forms 
from django.core.paginator import Paginator
from django.contrib import messages
import json
import datetime
from django.utils.timezone import utc


from .forms import (
    RegisterMerchantForm, 
    MerchantUpdateForm,
    MerchantAddressUpdateForm,
    MerchantParcelAddForm,
    MerchantParcelUpdateForm,
    MerchantParcelRemoveForm,
)

from express.models import Merchant
from express.models import Parcel
from addresses.models import Address


@login_required
def express_home_view(request):
    merchants = Merchant.objects.filter(user=request.user).order_by('-id')
    if not merchants:
        return HttpResponseRedirect(reverse('express:register_merchant'))
    #paginator
    paginator=Paginator(merchants,1)
    page_number=request.GET.get('page')
    merchant_page=paginator.get_page(page_number)
    
    print(merchants)

    context = {
        'page_context': {
            'title': "Express",
            'breadcrumb_active': "Home",
            'main_heading': "Express Home",
        },
        'merchant_username':'h',
        'merchants': merchant_page,
        'total_merchants':merchants.count(),
    }
    return render(request, 'express/express_home.html', context)


@login_required
def register_merchant_view(request):
    form = RegisterMerchantForm(request.POST or None, request.FILES or None)
    business_address_form = MerchantAddressUpdateForm(request.POST or None, request.FILES or None)
    pickup_address_form = MerchantAddressUpdateForm(request.POST or None, request.FILES or None)
    if request.method =='POST':
        if form.is_valid() and business_address_form.is_valid() and pickup_address_form.is_valid():
            # create merchant instance
            merchant = form.save(commit=False)
            # set business_address
            business_address = business_address_form.save(commit=False)
            business_address.address_type = Address.ADDRESS_TYPE_PARMANENT
            business_address.save()
            if business_address:
                merchant.business_address = business_address
            # set pickup_address
            pickup_address = pickup_address_form.save(commit=False)
            pickup_address.address_type = Address.ADDRESS_TYPE_PARMANENT
            pickup_address.save()
            if pickup_address:
                merchant.pickup_address = pickup_address
            merchant.user = request.user
            merchant.save()
            
            return HttpResponseRedirect(merchant.get_express_merchant_detail_url())
    context = {
        'page_context': {
            'title': "Register Merchant",
            'breadcrumb_active': "Register Merchant",
            'main_heading': "Register Merchant",
        },
        'form': form,
        'business_address_form': business_address_form,
        'pickup_address_form': pickup_address_form,
    }
    return render(request, 'express/register_merchant.html', context)

@login_required
def merchant_billing_account_view(request, merchant_username):
    merchant = get_object_or_404(Merchant, username=merchant_username.lower())
    pass



@login_required
def merchant_detail_view(request, merchant_username):
    merchant = get_object_or_404(Merchant, username=merchant_username.lower())
    parcels = Parcel.objects.filter(merchant=merchant).order_by('-id')
    
    #paginator
    paginator=Paginator(parcels,2)
    page_number=request.GET.get('page')
    parcel_page=paginator.get_page(page_number)

    context = {
        'page_context': {
            'title': merchant.business_name,
            'breadcrumb_active': "Merchant Details",
            'main_heading': merchant.business_name,
        },
        'merchant': merchant,
        'parcels': parcel_page,
        'total_parcel':parcels.count(),
        'req':''
    }
    return render(request, 'express/merchant_detail.html', context)


@login_required
def merchant_update_view(request, merchant_username):
    merchant = get_object_or_404(Merchant, username=merchant_username)
    
    form = MerchantUpdateForm(request.POST or None, request.FILES or None, instance=merchant)
    business_address_form = MerchantAddressUpdateForm(request.POST or None, request.FILES or None, instance=merchant.business_address)
    pickup_address_form = MerchantAddressUpdateForm(request.POST or None, request.FILES or None, instance=merchant.pickup_address)
    
    # payment_accounts

    if request.method =='POST':
        if form.is_valid() and business_address_form.is_valid() and pickup_address_form.is_valid():
            business_address = business_address_form.save()
            pickup_address = pickup_address_form.save()
            merchant = form.save(commit=False)
            if business_address:
                merchant.business_address = business_address
            if pickup_address:
                merchant.pickup_address = pickup_address
            merchant.save()
            messages.add_message(request,messages.SUCCESS,"Your Merchant Updated!")
            return HttpResponseRedirect(merchant.get_express_merchant_detail_url())
    
    context = {
        'page_context': {
            'title': "Merchant Update",
            'breadcrumb_active': "Merchant Update",
            'main_heading': "Merchant Update",
        },
        'merchant': merchant,
        'form': form,
        'business_address_form': business_address_form,
        'pickup_address_form': pickup_address_form,
    }
    return render(request, 'express/merchant_update.html', context)


@login_required
def merchant_parcel_list_view(request, merchant_username):
    merchant = get_object_or_404(Merchant, username=merchant_username)
    parcels = Parcel.objects.filter(merchant=merchant)

    context = {
        'page_context': {
            'title': f"{merchant.business_name}'s parcels",
            'breadcrumb_active': "Parcels",
            'main_heading': f"All Parcels of {merchant.business_name}",
        },
        'merchant': merchant,
        'parcels': parcels,
    }
    return render(request, 'express/merchant_parcel_list.html', context)


@login_required
def merchant_parcel_add_view(request, merchant_username):
    merchant = get_object_or_404(Merchant, username=merchant_username)
    merchant_parcel_form = MerchantParcelAddForm(request.POST or None, request.FILES or None)
    shipping_address_form = MerchantAddressUpdateForm(request.POST or None, request.FILES or None)
    
    if request.method =='POST':
        if merchant_parcel_form.is_valid() and shipping_address_form.is_valid():
            merchant_parcel = merchant_parcel_form.save(commit=False)
            # set parcel's merchant
            merchant_parcel.merchant = merchant
            # set shipping_address
            shipping_address = shipping_address_form.save(False)
            shipping_address.address_type = Address.ADDRESS_TYPE_SHIPPING
            shipping_address.save()
            if shipping_address:
                merchant_parcel.shipping_address = shipping_address

            if merchant_parcel.is_ordered == True:
                # set the ordered_date
                merchant_parcel.ordered_date = datetime.datetime.utcnow().replace(tzinfo=utc)
            merchant_parcel.save()
            return HttpResponseRedirect(merchant_parcel.get_express_merchant_parcel_detail_url())

    context = {
        'page_context': {
            'title': merchant.business_name,
            'breadcrumb_active': "Parcel Add",
            'main_heading': f"Add parcel to {merchant.business_name}",
        },
        'merchant': merchant,
        'merchant_parcel_form': merchant_parcel_form,
        'shipping_address_form': shipping_address_form,
    }
    return render(request, 'express/merchant_parcel_add.html', context)


@login_required
def merchant_parcel_detail_view(request, merchant_username, parcel_id):
    merchant = get_object_or_404(Merchant, username=merchant_username)
    parcel = get_object_or_404(Parcel, id=parcel_id, merchant=merchant)
    context = {
        'page_context': {
            'title': merchant.business_name,
            'breadcrumb_active': "Parcel Detail",
            'main_heading': parcel.id,
        },
        'merchant': merchant,
        'parcel': parcel,
    }
    return render(request, 'express/merchant_parcel_detail.html', context)


@login_required
def merchant_parcel_update_view(request, merchant_username, parcel_id):
    merchant = get_object_or_404(Merchant, username=merchant_username)
    parcel = get_object_or_404(Parcel, id=parcel_id, merchant=merchant)

    parcel_update_form = MerchantParcelUpdateForm(request.POST or None, request.FILES or None, instance=parcel)
    shipping_address_form = MerchantAddressUpdateForm(request.POST or None, request.FILES or None, instance=parcel.shipping_address)
    
    if request.method =='POST':
        if parcel_update_form.is_valid() and shipping_address_form.is_valid():
            shipping_address = shipping_address_form.save()
            parcel = parcel_update_form.save(commit=False)
            if shipping_address:
                parcel.shipping_address = shipping_address
            parcel.save()
            messages.add_message(request,messages.SUCCESS,"Your Parcel Updated!")
            return HttpResponseRedirect(parcel.get_express_merchant_parcel_detail_url())

    context = {
        'page_context': {
            'title': merchant.business_name,
            'breadcrumb_active': "Parcel Update",
            'main_heading': "Parcel Update",
        },
        'merchant': merchant,
        'parcel': parcel,
        'parcel_update_form': parcel_update_form,
        'shipping_address_form': shipping_address_form,
    }
    return render(request, 'express/merchant_parcel_update.html', context)


@login_required
def merchant_parcel_remove_view(request, merchant_username, parcel_id):
    merchant = get_object_or_404(Merchant, username=merchant_username)
    parcel = get_object_or_404(Parcel, id=parcel_id, merchant=merchant)

    parcel_remove_form = MerchantParcelRemoveForm(request.POST or None, request.FILES or None, instance=parcel)
    
    # if request.method =='POST':
        # if parcel_remove_form.is_valid():
    parcel = parcel_remove_form.save()
    messages.add_message(request,messages.ERROR,"Your Parcel Removed!")
    
    return HttpResponseRedirect(merchant.get_express_merchant_detail_url())
