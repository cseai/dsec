from django.http import HttpResponse
from django.shortcuts import render
from  home.popular_cousine import POPULAR_COUSINE


def home_page(request):
    
    # festival_list = [("Birthday",1), ('Holi',2), ('Diwali',3)]

    context={
        "popular_cousine":POPULAR_COUSINE,
    }
    return render(request, 'home/index.html',context)
