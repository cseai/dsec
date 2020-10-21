from django.http import HttpResponse
from django.shortcuts import render

from .helpers import get_urls

# import types

# from django.urls import get_resolver

def dev_home(request):
    url_list_dict, url_dict_list = get_urls()
    try:
        dev_urls = url_dict_list['dev']
        urls = {
            'dev': dev_urls
        }
    except:
        urls = url_dict_list
    context = {
        'title': 'Dev Home',
        'urls': urls,
    }
    return render(request, 'dev/dev_home.html', context)

def show_urls(request):
    url_list_dict, url_dict_list = get_urls()
    urls = url_dict_list
    # print(urls)
    context = {
        'title': 'All URLs',
        'urls': urls,
    }
    return render(request, 'dev/show_urls.html', context)