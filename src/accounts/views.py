from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, FormView, DetailView, View, UpdateView
from django.shortcuts import render,redirect

from core.mixins import NextUrlMixin, RequestFormAttachMixin


#LoginRequiredMixin,
class AccountHomeView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/account_home.html'
    def get_object(self):
        return self.request.user