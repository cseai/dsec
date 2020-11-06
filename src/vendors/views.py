from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render, reverse, get_object_or_404
from django import forms 
from django.core.paginator import Paginator
import json
from .forms import (
    RegisterStoreForm, 
    StoreUpdateForm,
    StoreAddressUpdateForm,
    StoreStatusUpdateForm,
    StoreProductAddForm,
    StoreProductUpdateForm,
    StoreProductRemoveForm,
)

from vendors.models import Store
from addresses.models import Address
from products.models import Product


@login_required
def vendor_home_view(request):

    stores = Store.objects.filter(user=request.user).order_by('-id')
    
    #paginator
    paginator=Paginator(stores,1)
    page_number=request.GET.get('page')
    store_page=paginator.get_page(page_number)
    
    
    context = {
        'page_context': {
            'title': "Vendor",
            'breadcrumb_active': "Home",
            'main_heading': "Vendor Home",
        },
        'stores': store_page,
        'total_stores':stores.count(),
    }
    return render(request, 'vendors/vendor_home.html', context)



@login_required
def register_store_view(request, *args, **kwargs):
    
    form = RegisterStoreForm(request.POST or None, request.FILES or None)
    
    if request.method =='POST':
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # title = form.cleaned_data.get('title')
            # category = form.cleaned_data.get('category')
            # opening_time = form.cleaned_data.get('opening_time')
            # closing_time = form.cleaned_data.get('closing_time')
            
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
                    address_type=Address.ADDRESS_TYPE_PARMANENT,
                    line_1=address_line_1,
                    line_2=address_line_2,
                    city=city,
                    state=state,
                    postal_code=postal_code,
                    country=country
                )
            except:
                # raise forms.ValidationError("Invalid Address Information!")
                address = None
            
            # create store instance
            store = form.save(commit=False)
            if address:
                store.address = address
            store.user = request.user
            store.save()
            
            return HttpResponseRedirect(reverse('vendors:store_detail'))
    context = {
        'page_context': {
            'title': "Register Store",
            'breadcrumb_active': "Register Store",
            'main_heading': "Register Store",
        },
        'form': form,
    }
    return render(request, 'vendors/register_store.html', context)

@login_required
def store_detail_view(request, store_username, *args, **kwargs):
        
    store = get_object_or_404(Store, username=store_username)
    products = Product.objects.filter(store=store).order_by('-id')
    
    #paginator
    paginator=Paginator(products,2)
    page_number=request.GET.get('page')
    product_page=paginator.get_page(page_number)

    store_status_form = StoreStatusUpdateForm(request.POST or None, request.FILES or None, instance=store)
    if request.method =='POST':
        if store_status_form.is_valid():
            store = store_status_form.save()
            store.save()
    context = {
        'page_context': {
            'title': store.title,
            'breadcrumb_active': "Store Details",
            'main_heading': store.title,
        },
        'store': store,
        'store_status_form': store_status_form,
        'products': product_page,
        'total_product':products.count(),
    }
    return render(request, 'vendors/store_detail.html', context)


@login_required
def store_update_view(request, store_username):
    store = get_object_or_404(Store, username=store_username)
    
    form = StoreUpdateForm(request.POST or None, request.FILES or None, instance=store)
    store_address_form = StoreAddressUpdateForm(request.POST or None, request.FILES or None, instance=store.address)
    
    if request.method =='POST':
        if form.is_valid() and store_address_form.is_valid():
            store_address = store_address_form.save()
            store = form.save(commit=False)
            if store_address:
                store.address = store_address
            store.save()
            
            return HttpResponseRedirect(reverse('vendors:store_detail', kwargs={'store_username': store.username}))
    context = {
        'page_context': {
            'title': "Store Update",
            'breadcrumb_active': "Store Update",
            'main_heading': "Store Update",
        },
        'form': form,
        'store_address_form': store_address_form,
    }
    return render(request, 'vendors/store_update.html', context)


@login_required
def store_product_list_view(request, store_username):
    store = get_object_or_404(Store, username=store_username)
    store_products = Product.objects.filter(store=store)

    context = {
        'page_context': {
            'title': "store_product_list",
            'breadcrumb_active': "",
            'main_heading': "store_product_list",
        },
        'store': store,
        'store_products': store_products,
    }
    return render(request, 'vendors/store_product_list.html', context)


@login_required
def store_product_add_view(request, store_username):
    store = get_object_or_404(Store, username=store_username)
    store_product_form = StoreProductAddForm(request.POST or None, request.FILES or None)
    
    if request.method =='POST':
        if store_product_form.is_valid():
            store_product = store_product_form.save(commit=False)
            # set product's store
            store_product.store = store
            store_product.save()
            return HttpResponseRedirect(reverse('vendors:store_detail', kwargs={'store_username': store.username }))

    context = {
        'page_context': {
            'title': store.title,
            'breadcrumb_active': "Product Add",
            'main_heading': f"Add product to {store.title}",
        },
        'store': store,
        'store_product_form': store_product_form,
    }
    return render(request, 'vendors/store_product_add.html', context)


@login_required
def store_product_detail_view(request, store_username, product_id):
    store = get_object_or_404(Store, username=store_username)
    store_product = get_object_or_404(Product, id=product_id, store=store)
    context = {
        'page_context': {
            'title': store.title,
            'breadcrumb_active': "Product Detail",
            'main_heading': store_product.title,
        },
        'store': store,
        'store_product': store_product,
    }
    return render(request, 'vendors/store_product_detail.html', context)


@login_required
def store_product_update_view(request, store_username, product_id):
    store = get_object_or_404(Store, username=store_username)
    store_product = get_object_or_404(Product, id=product_id, store=store)

    store_product_form = StoreProductUpdateForm(request.POST or None, request.FILES or None, instance=store_product)
    
    if request.method =='POST':
        if store_product_form.is_valid():
            print("product update --->>>>")
            store_product = store_product_form.save()
            return HttpResponseRedirect(reverse('vendors:store_detail', kwargs={'store_username': store.username,}))

    context = {
        'page_context': {
            'title': store.title,
            'breadcrumb_active': "Product Update",
            'main_heading': "Product Update",
        },
        'store': store,
        'store_product': store_product,
        'store_product_form': store_product_form,
    }
    return render(request, 'vendors/store_product_update.html', context)


@login_required
def store_product_remove_view(request, store_username, product_id):
    store = get_object_or_404(Store, username=store_username)
    store_product = get_object_or_404(Product, id=product_id, store=store)

    store_product_form = StoreProductRemoveForm(request.POST or None, request.FILES or None, instance=store_product)
    
    if request.method =='POST':
        if store_product_form.is_valid():
            store_product = store_product_form.save()
            return HttpResponseRedirect(reverse('vendors:store_product_list', kwargs={'store_username': store.username}))

    context = {
        'page_context': {
            'title': store.title,
            'breadcrumb_active': "Product Remove",
            'main_heading': f"Confirm Remove Product: {store_product.title}",
        },
        'store': store,
        'store_product': store_product,
        'store_product_form': store_product_form,
    }
    return render(request, 'vendors/store_product_remove.html', context)



#api
def api_store_product_detail_view(request):
    if request.is_ajax() and request.method == 'GET':  
        print("hello there")
        store_username = request.GET['store_username']
        store_product_id = request.GET['product_id']
        
        try:
            store = Store.objects.get(username=store_username)
            product = store.product_set.get(id=store_product_id)
            print(product)
            data={
                'status' : '200',
                'title' : str(product.title),
                'image' : str(product.image.url),
                'description' : str(product.description),
                'sup_price' : int(product.sup_price),
                'selling_price' : int(product.selling_price),
            }
            return HttpResponse(json.dumps(data))
        except:
            data={
                'status':'404',
            }
            return HttpResponse(json.dumps(data))
        