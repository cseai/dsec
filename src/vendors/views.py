from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render, reverse, get_object_or_404
from django import forms 
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
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
    queryset_list = Store.objects.filter(user=request.user).filter(is_active=True).order_by('id')

    # Ordering
    select_order_by = {
        'label': "Sort by",
        'name': "order_by",
        'choices': {
            'id': "Default",
            'username': "Username",
            'title': "Title",
            'category': "Category",
            'timestamp': "Timestamp (Leatest)",
            '-timestamp': "Timestamp (Oldest)",
            'updated': "Updated (Leatest)",
            '-updated': "Updated (Oldest)",
        },
    }
    order_by = request.GET.get(select_order_by.get('name'))
    if order_by and order_by in select_order_by.get('choices'):
        queryset_list = queryset_list.order_by(order_by)
    

    # filtering
    search_filter = {
        'label': "Search",
        'name': "search",
        'placeholder': "Store Name \ Username OR IDs",
        'search_by': {
            'label': "Search By",
            'name': "search_by",
            'choices': {
                'default': "Default",
                'ids': "IDs",
            },
        },
        # some search related context data
        'context': {
            'sc': "",
            'req': "",
        }
    }
    query = request.GET.get(search_filter.get('name'))
    if query:
        # some search related context data
        search_filter['context']['sc'] = query
        search_filter['context']['req'] = "req"

        search_by_choice = request.GET.get(search_filter.get("search_by").get("name"))
        if search_by_choice and search_by_choice in search_filter.get("search_by").get("choices"):
            if search_by_choice == 'default':
                queryset_list = queryset_list.filter(
                    Q(title__icontains=query) |
                    Q(username__iexact=query)
                ).distinct()
            elif search_by_choice == 'ids':
                try:
                    queryset_list = queryset_list.filter(
                        Q(pk__in=query.split(',')) 
                    ).distinct()
                except:
                    queryset_list = queryset_list.none()
        else:
            queryset_list = queryset_list.none()

    # pagination
    pagination_filter = {
        'select_show_per_page': {
            'label': "View",
            'name': "per_page",
            'choices': list(range(5, queryset_list.count()+5, 5)),
        },
        'page_request_var': "page",
    }
    max_obj_per_page = request.GET.get(pagination_filter.get('select_show_per_page').get('name'))
    if max_obj_per_page and max_obj_per_page.isnumeric() and int(max_obj_per_page) in pagination_filter.get("select_show_per_page").get('choices'):
        max_obj_per_page = int(max_obj_per_page)
    else:
        max_obj_per_page = 5
    paginator = Paginator(queryset_list, max_obj_per_page)

    page_number = request.GET.get(pagination_filter.get('page_request_var'))
    if page_number and page_number.isnumeric():
        page_number = int(page_number)
    else:
        page_number = 1
    queryset = paginator.get_page(page_number)

    
    context = {
        'page_context': {
            'title': "Vendor",
            'breadcrumb_active': "Home",
            'main_heading': "Vendor Home",
        },
        'filter_form': {
            'method': "GET",
            'select_order_by': select_order_by,
            'search_filter': search_filter,
            'pagination_filter': pagination_filter,
        },
        'stores': queryset,
        'total_stores': paginator.count,
        'sc': search_filter.get('context').get("sc"),
        'req': search_filter.get('context').get("req"),
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
    store = get_object_or_404(Store, username=store_username.lower())
    queryset_list = Product.objects.filter(store=store).filter(active=True).order_by('-id')

    # Ordering
    select_order_by = {
        'label': "Sort by",
        'name': "order_by",
        'choices': {
            'id': "Default",
            'title': "Title",
            'sku': "SKU",
            'manufacturer': "Manufacturer",
            'sup_price': "Supply price (Low)",
            '-sup_price': "Supply price (High)",
            'selling_price': "Selling price (Low)",
            '-selling_price': "Selling price (High)",
            'timestamp': "Timestamp (Leatest)",
            '-timestamp': "Timestamp (Oldest)",
            'updated': "Updated (Leatest)",
            '-updated': "Updated (Oldest)",
        },
    }
    order_by = request.GET.get(select_order_by.get('name'))
    if order_by and order_by in select_order_by.get('choices'):
        queryset_list = queryset_list.order_by(order_by)
    

    # filtering
    search_filter = {
        'label': "Search",
        'name': "search",
        'placeholder': "Food Name\Tag\Cuisine\SKU\Manufacturer OR IDs",
        'search_by': {
            'label': "Search By",
            'name': "search_by",
            'choices': {
                'default': "Default",
                'ids': "IDs",
            },
        },
        # some search related context data
        'context': {
            'sc': "",
            'req': "",
        }
    }
    query = request.GET.get(search_filter.get('name'))
    if query:
        # some search related context data
        search_filter['context']['sc'] = query
        search_filter['context']['req'] = "req"

        search_by_choice = request.GET.get(search_filter.get("search_by").get("name"))
        if search_by_choice and search_by_choice in search_filter.get("search_by").get("choices"):
            if search_by_choice == 'default':
                queryset_list = queryset_list.filter(
                    Q(title__icontains=query) |
                    Q(tags__name__in=query.split(',')) |
                    Q(cuisine__title__iexact=query) |
                    Q(sku__iexact=query) |
                    Q(manufacturer__iexact=query)
                ).distinct()
            elif search_by_choice == 'ids':
                try:
                    queryset_list = queryset_list.filter(
                        Q(pk__in=query.split(',')) 
                    ).distinct()
                except:
                    queryset_list = queryset_list.none()
        else:
            queryset_list = queryset_list.none()

    # pagination
    pagination_filter = {
        'select_show_per_page': {
            'label': "View",
            'name': "per_page",
            'choices': list(range(5, queryset_list.count()+5, 5)),
        },
        'page_request_var': "page",
    }
    max_obj_per_page = request.GET.get(pagination_filter.get('select_show_per_page').get('name'))
    if max_obj_per_page and max_obj_per_page.isnumeric() and int(max_obj_per_page) in pagination_filter.get("select_show_per_page").get('choices'):
        max_obj_per_page = int(max_obj_per_page)
    else:
        max_obj_per_page = 5
    paginator = Paginator(queryset_list, max_obj_per_page)

    page_number = request.GET.get(pagination_filter.get('page_request_var'))
    if page_number and page_number.isnumeric():
        page_number = int(page_number)
    else:
        page_number = 1
    queryset = paginator.get_page(page_number)

    context = {
        'page_context': {
            'title': store.title,
            'breadcrumb_active': "Store Details",
            'main_heading': store.title,
        },
        'filter_form': {
            'method': "GET",
            'select_order_by': select_order_by,
            'search_filter': search_filter,
            'pagination_filter': pagination_filter,
        },
        'store': store,
        'products': queryset,
        'total_product': paginator.count,
        'sc': search_filter.get('context').get("sc"),
        'req': search_filter.get('context').get("req"),
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
            messages.add_message(request,messages.SUCCESS,"Your Store Updated!")
            return HttpResponseRedirect(reverse('vendors:store_detail', kwargs={'store_username': store.username}))
    
    context = {
        'page_context': {
            'title': "Store Update",
            'breadcrumb_active': "Store Update",
            'main_heading': "Store Update",
        },
        'store': store,
        'form': form,
        'store_address_form': store_address_form,
    }
    return render(request, 'vendors/store_update.html', context)


@login_required
def store_product_list_view(request, store_username):
    store = get_object_or_404(Store, username=store_username)
    products = Product.objects.filter(store=store)

    context = {
        'page_context': {
            'title': f"{store.title}'s products",
            'breadcrumb_active': "Products",
            'main_heading': "All Products",
        },
        'store': store,
        'products': products,
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
            # If saving a form using [commit=False] Without this next line the tags won't be saved.
            store_product_form.save_m2m()
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
    return render(request, 'vendors/store_product_detail.html', context)


@login_required
def store_product_update_view(request, store_username, product_id):
    
    store = get_object_or_404(Store, username=store_username)
    product = get_object_or_404(Product, id=product_id, store=store)

    product_update_form = StoreProductUpdateForm(request.POST or None, request.FILES or None, instance=product)
    
    if request.method =='POST':
        if product_update_form.is_valid():
            product = product_update_form.save()
            # If saving a form using [commit=False] Without this next line the tags won't be saved.
            product_update_form.save_m2m()
            messages.add_message(request,messages.SUCCESS,"Your Product Updated!")
            return HttpResponseRedirect(reverse('vendors:store_detail', kwargs={'store_username': store.username,}))

    context = {
        'page_context': {
            'title': store.title,
            'breadcrumb_active': "Product Update",
            'main_heading': "Product Update",
        },
        'store': store,
        'product': product,
        'product_update_form': product_update_form,
    }
    return render(request, 'vendors/store_product_update.html', context)


@login_required
def store_product_remove_view(request, store_username, product_id):
    store = get_object_or_404(Store, username=store_username)
    product = get_object_or_404(Product, id=product_id, store=store)

    product_remove_form = StoreProductRemoveForm(request.POST or None, request.FILES or None, instance=product)
    
    # if request.method =='POST':
        # if product_remove_form.is_valid():
    product = product_remove_form.save()
    messages.add_message(request,messages.ERROR,"Your Product Removed!")
    
    return HttpResponseRedirect(reverse('vendors:store_detail', kwargs={'store_username': store.username}))

    # context = {
    #     'page_context': {
    #         'title': store.title,
    #         'breadcrumb_active': "Product Remove",
    #         'main_heading': f"Confirm Remove Product: {product.title}",
    #     },
    #     'store': store,
    #     'product': product,
    #     'product_remove_form': product_remove_form,
    # }
    # return render(request, 'vendors/store_product_remove.html', context)



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
        
        
def api_store_status_update(request):
    if request.method == 'POST' and request.is_ajax():

        # get store username
        store_username = request.POST.get('store_username')
        curr_state = request.POST.get('curr_state')
        
        if curr_state == 'open':
            print("current state : ",curr_state)
            store = Store.objects.filter(user=request.user).get(username=store_username)
            print(store.is_open)
            if store.is_open:
                try:
                    store.is_open=False;
                    store.save()
                    data={
                        'status':'200',
                        'msg':"Your Store Closed!",
                    }
                    # messages.add_message(request,messages.ERROR,"Your Store Closed!")
                    return HttpResponse(json.dumps(data))
                except :
                    data={
                        'status':'500',
                        'msg':"Opps Somethings Went Wrong!",
                    }
                    # messages.add_message(request,messages.ERROR,"Your Store Closed!")
                    return HttpResponse(json.dumps(data))
        
        elif curr_state == 'close':
            print("current state : ",curr_state)
            
            store = Store.objects.filter(user=request.user).get(username=store_username)
            
            if store.is_open == False:
                print(store.is_open)
                try:
                    store.is_open=True;
                    store.save()
                    data={
                        'status':'200',
                        'msg':"Your Store Open Now!",
                    }
                    return HttpResponse(json.dumps(data))
                except:
                    data={
                        'status':'500',
                        'msg':"Opps Somethings Went Wrong!",
                    }
                    return HttpResponse(json.dumps(data))
                
            
        
        else:
            data={
                'status':'404',
                'msg':"Opps Somethings Went Wrong!",
            }
            
            return HttpResponse(json.dumps(data))
        
        
        