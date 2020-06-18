from django.shortcuts import render
from django.http import HttpResponse
from . import models, utils, handlers


def index(request):
    return HttpResponse('<h1>aloha!</h1>')


def register_user(request):
    return handlers.AuthHandler.register_user(request)


def login(request):
    return handlers.AuthHandler.login(request)


def home(request):
    if handlers.AuthHandler.access_granted(request, ['company', 'candidate']):
        if handlers.AuthHandler.get_curr_profile(request).role == 'company':
            return handlers.CompanyHandler.dash(request)
    else:
        return render(request, 'jobs/403.html')


def position_create(request):
    if handlers.AuthHandler.access_granted(request, 'company'):
        return handlers.PositionHandler.create(request)
    else:
        return render(request, 'jobs/403.html')
