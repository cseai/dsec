from django.shortcuts import render,redirect
from vendors.models import Store
from .forms import StoreForm
# Create your views here.
def index(request):
    return render(request,'adminPanel/base.html')

def all_store_request(request):
    context={}
    stores=Store.objects.all().filter(is_verified=False)
    context={
        'all_store':stores,
    }
    print(stores)
    
    return render(request,'adminPanel/store/all_store_request.html',context)

def store_details(request,store_id):
    context={}
    store=Store.objects.get(id=store_id)
    form=StoreForm(instance=store)
    if request.method=='POST':
        form=StoreForm(request.POST or None,request.FILES or None,instance=store)
        if form.is_valid():
            form.save()
            return redirect('adminpanel:store_request')
    
    context={
        'store':store,
        'form':form
    }
    return render(request,'adminPanel/store/store_details.html',context)