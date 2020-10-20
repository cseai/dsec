from django.shortcuts import render,redirect
from vendors.models import Store
from .forms import (StoreFormDisable,StoreForm)
from .choices import state_choices
# Create your views here.
def index(request):
    return render(request,'adminPanel/base.html')

def all_store(request):
    key='all'
    search=''
    context={}
    
    stores=Store.objects.all().filter(is_active=True).filter(is_verified=True)
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
    return render(request,'adminPanel/store/all_store.html',context)

def all_store_request(request):
    key='all'
    search=''
    context={}
    #query
    stores=Store.objects.all().filter(is_verified=False).filter(is_active=False)
    
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
        return render(request,'adminPanel/store/all_store_request.html',context)
    
    context={
        'all_store':stores,
        'state_choices':state_choices,
        'key':key,
        'sc':search,
    }
    return render(request,'adminPanel/store/all_store_request.html',context)

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

def store_details(request,store_id):
    context={}
    store=Store.objects.get(id=store_id)
    form=StoreFormDisable(instance=store)
    
    context={
        'store':store,
        'form':form
    }
    return render(request,'adminPanel/store/store_details.html',context)


def store_delete(request,store_id):
    delete=Store.objects.get(id=store_id).delete()
    return redirect('adminpanel:store_request')