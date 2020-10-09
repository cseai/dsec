from django.http import HttpResponse
from django.shortcuts import render


def home_page(request):
    return render(request, 'home/index.html')


def login_test(request):
    return render(request, 'auth/auth.html')
