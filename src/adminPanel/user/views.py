from django.shortcuts import render,redirect
from accounts.models import User
from adminPanel.choices import (user_choices)
from .forms import UserFormDisable

def all_user(request):
    context={}
    key='all'
    search=''
    
    users=User.objects.all().filter(is_admin=False)
    
    if request.method=='GET':
        #search area
        if 'keyword' in request.GET:
            key=request.GET.get('keyword')
            if key=='name':
                if 'search' in request.GET:
                    search=request.GET.get('search')
                    users=users.filter(first_name__icontains=search)
                    # print(stores)
            elif key=='phone':
                search=request.GET.get('search')
                users=users.filter(phone__icontains=search)
            elif key=='email':
                search=request.GET.get('search')
                users=users.filter(email__icontains=search)
            elif key=='active':
                users=users.filter(is_active=True)
            elif key=='deactive':
                users=users.filter(is_active=False)
            elif key=='verified':
                users=users.filter(is_verified=True)
            elif key=='notverified':
                users=users.filter(is_verified=False)
            elif key=='gender_m':
                users=users.filter(gender='M')
            elif key=='gender_f':
                users=users.filter(gender='F')
            elif key=='all':
                pass
        
        context={
            'users':users,
            'key':key,
            'sc':search,
            'user_choices':user_choices
        }
        return render(request,'adminPanel/user/user.html',context)
    
    context={
        'users':users,
        'user_choices':user_choices,
        'key':key,
        'sc':search,
    }

    return render(request,'adminPanel/user/user.html',context)


def user_details(request,user_id):
    context={}
    user=User.objects.get(id=user_id)
    form=UserFormDisable(instance=user)
    
    context={
        'user':user,
        'form':form
    }
    return render(request,'adminPanel/user/user_details.html',context)


# #f00 not complete
def user_details_update(request,store_id):
    context={}
    user=User.objects.get(id=store_id)
    form=UserForm(instance=store)
    if request.method=='POST':
        form=UserForm(request.POST or None,request.FILES or None,instance=store)
        if form.is_valid():
            # store=form.save(commit=False)
            # store.is_active=True
            # store.is_verified=True
            # store.save()
            return redirect('adminpanel:adminpanel_user:all_user')
    
    context={
        'user':user,
        'form':form
    }
    return render(request,'adminPanel/user/user_details.html',context)
