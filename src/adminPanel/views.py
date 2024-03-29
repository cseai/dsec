from django.shortcuts import render,redirect
from django.contrib import messages
from vendors.models import Store
from .forms import (StoreFormDisable,StoreForm)
from .choices import state_choices
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    return render(request,'adminPanel/base.html')

def all_store(request):
    key='all'
    search=''
    context={}
    
    
    stores=Store.objects.all().filter(is_active=True).filter(is_verified=True)
    
    #paginator
    paginator=Paginator(stores,1)
    page_number=request.GET.get('page')
    obj_page=paginator.get_page(page_number)
    
    if 'sc_btn' in request.GET:
        #search area
        if 'keyword' in request.GET:
            key=request.GET.get('keyword')
            if key=='title':
                if 'search' in request.GET:
                    search=request.GET.get('search')
                    stores=stores.filter(title__icontains=search)
                    # print(stores)
            elif key=='all':
                pass
        
        # paginator
        paginator=Paginator(stores,1)
        page_number=request.GET.get('page')
        page_obj=paginator.get_page(page_number)
        
        context={
            'all_store':page_obj,
            'key':key,
            'sc':search,
            'state_choices':state_choices,
            'req':'req'
        }
        return render(request,'adminPanel/store/all_store.html',context)
    
    context={
        'all_store':obj_page,
        'state_choices':state_choices,
        'key':key,
        'sc':search,
        'req':''
    }
    
    return render(request,'adminPanel/store/all_store.html',context)


def all_store_request(request):
    key='all'
    search=''
    context={}
    # message test
    messages.add_message(request, messages.ERROR, 'Hello world.')
    #query
    stores=Store.objects.all().filter(is_verified=False).order_by('id')
    # paginator
    paginator=Paginator(stores,2)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    
    #search area
    
    if 'sc_btn' in request.GET:
        print("Hello")
        if 'keyword' in request.GET:
            key=request.GET.get('keyword')
            if key=='title':
                if 'search' in request.GET:
                    search=request.GET.get('search')
                    stores=stores.filter(title__icontains=search)
                    # print(stores)
            elif key=='all':
                pass
            
            # paginator
            paginator=Paginator(stores,2)
            page_number=request.GET.get('page')
            page_obj=paginator.get_page(page_number)
            
            context={
                'all_store':page_obj,
                'key':key,
                'sc':search,
                'state_choices':state_choices,
                'req':'req'
            }
            return render(request,'adminPanel/store/all_store_request.html',context)
        
    context={
        'all_store':page_obj,
        'state_choices':state_choices,
        'key':key,
        'sc':search,
        'req':''
    }
    
    return render(request,'adminPanel/store/all_store_request.html',context)



def store_details(request,store_id):
    context={}
    store=Store.objects.get(id=store_id)
    form=StoreFormDisable(instance=store)
    
    context={
        'store':store,
        'form':form
    }
    return render(request,'adminPanel/store/store_details.html',context)


def store_details_update(request,store_id):
    context={}
    store=Store.objects.get(id=store_id)
    form=StoreForm(instance=store)
    if request.method=='POST':
        form=StoreForm(request.POST or None,request.FILES or None,instance=store)
        if form.is_valid():
            store=form.save(commit=False)
            store.is_active=True
            store.is_verified=True
            store.save()
            return redirect('adminpanel:store_request')
    
    context={
        'store':store,
        'form':form
    }
    return render(request,'adminPanel/store/store_details.html',context)

def store_deactived(request):
    key='all'
    search=''
    context={}
    
    stores=Store.objects.all().filter(is_active=False).filter(is_verified=True)
    if request.method=='GET':
        #search area
        if 'keyword' in request.GET:
            key=request.GET.get('keyword')
            if key=='title':
                if 'search' in request.GET:
                    search=request.GET.get('search')
                    stores=stores.filter(title__icontains=search)
                    # print(stores)
            elif key=='all':
                pass
        
        context={
            'all_store':stores,
            'key':key,
            'sc':search,
            'state_choices':state_choices
        }
        return render(request,'adminPanel/store/all_store.html',context)
    
    context={
        'all_store':stores,
        'state_choices':state_choices,
        'key':key,
        'sc':search,
    }
    context={
        'all_store':stores,
    }
    return render(request,'adminPanel/store/store_deactive.html',context)

# deacative store
def store_deactive(request,store_id):
    store=Store.objects.get(id=store_id)
    store.is_active=False
    store.save()
    return redirect('adminpanel:store')

#store active
def store_active(request,store_id):
    store=Store.objects.get(id=store_id)
    store.is_active=True
    store.save()
    return redirect('adminpanel:store')

def store_delete(request,store_id):
    delete=Store.objects.get(id=store_id).delete()
    return redirect('adminpanel:store_request')