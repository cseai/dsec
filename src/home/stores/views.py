from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse, get_object_or_404
from django import forms 
from django.core.paginator import Paginator

from vendors.models import Store
from products.models import Product


def store_list_view(request):
    stores = Store.objects.all()
    context = {
        'page_context': {
            'title': "Stores",
            'breadcrumb_active': "All Stores",
            'main_heading': "Store List",
        },
        'stores': stores,
    }
    return render(request, 'home/stores/store_list.html', context)


def store_detail_view(request, store_username, *args, **kwargs):
    store = get_object_or_404(Store, username=store_username)
    products = Product.objects.filter(store=store)
    
    #paginator
    paginator=Paginator(products,1)
    page_number=request.GET.get('page')
    product_page=paginator.get_page(page_number)

    context = {
        'page_context': {
            'title': store.title,
            'breadcrumb_active': "Store Details",
            'main_heading': store.title,
        },
        'store': store,
        'products': product_page,
        'total_product': products.count(),
    }
    return render(request, 'home/stores/store_detail.html', context)


def store_product_list_view(request, store_username):
    store = get_object_or_404(Store, username=store_username)
    store_products = Product.objects.filter(store=store)

    context = {
        'page_context': {
            'title': store.title,
            'breadcrumb_active': "Products",
            'main_heading': f"Products of {store.title}",
        },
        'store': store,
        'store_products': store_products,
    }
    return render(request, 'home/stores/store_product_list.html', context)


def store_product_detail_view(request, store_username, product_id):
    store = get_object_or_404(Store, username=store_username)
    product = get_object_or_404(Product, id=product_id, store=store)
    context = {
        'page_context': {
            'title': store.title,
            'breadcrumb_active': "Product Detail",
            'main_heading': product.title,
        },
        'store': store,
        'product': product,
    }
    return render(request, 'home/stores/store_product_detail.html', context)


