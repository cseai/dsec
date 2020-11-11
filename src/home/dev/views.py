from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render

from .helpers import get_urls

from phone_verify.models import SMSVerification

from accounts.utils.decorators import allowed_users
User = get_user_model()

@allowed_users(allowed_roles=[User.Role.SUPER_ADMIN, User.Role.ADMIN])
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

def show_phone_verification_table(request):
    obj_list = SMSVerification.objects.all()
    context = {
        'obj_list': obj_list,
    }
    return render(request, 'dev/show_phone_verification_table.html', context)
