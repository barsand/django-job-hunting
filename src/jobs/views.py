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
        role = handlers.AuthHandler.get_curr_profile(request).role
        if role == 'company':
            return handlers.CompanyHandler.dash(request)
        elif role == 'candidate':
            return handlers.CandidateHandler.dash(request)

    else:
        return render(request, 'jobs/403.html')


def position_create(request):
    if handlers.AuthHandler.access_granted(request, 'company'):
        return handlers.PositionHandler.create(request)
    else:
        return render(request, 'jobs/403.html')


def position_view(request, position_id):
    if handlers.AuthHandler.access_granted(request, ['company', 'candidate']):
        role = handlers.AuthHandler.get_curr_profile(request).role
        if role == 'company':
            pass
        elif role == 'candidate':
            return handlers.CandidateHandler.position_view(request, position_id)

    else:
        return render(request, 'jobs/403.html')

def position_apply(request, position_id):
    if handlers.AuthHandler.access_granted(request, 'candidate'):
        return handlers.CandidateHandler.position_apply(request, position_id)

    else:
        return render(request, 'jobs/403.html')
