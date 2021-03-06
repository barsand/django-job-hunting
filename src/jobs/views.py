from django.shortcuts import render
from django.http import HttpResponse
from . import models, utils, handlers


def index(request):
    return HttpResponse('<h1>aloha!</h1>')


def register_user(request):
    return handlers.AuthHandler.register_user(request)


def login(request):
    return handlers.AuthHandler.login(request)


def logout(request):
    return handlers.AuthHandler.logout(request)

def home(request):
    if handlers.AuthHandler.access_granted(request, ['company', 'candidate']):
        role = handlers.AuthHandler.get_curr_profile(request).role
        if role == 'company':
            return handlers.CompanyHandler.dash(request)
        elif role == 'candidate':
            return handlers.CandidateHandler.dash(request)

    else:
        return render(request, 'jobs/403.html')

def reports(request):
    if handlers.AuthHandler.access_granted(request, 'company'):
        return handlers.ReportHandler.report_view(request)

    else:
        return render(request, 'jobs/403.html')


def position_create(request):
    if handlers.AuthHandler.access_granted(request, 'company'):
        return handlers.PositionHandler.position_create(request)
    else:
        return render(request, 'jobs/403.html')


def position_view(request, position_id):
    if handlers.AuthHandler.access_granted(request, ['company', 'candidate']):
        return handlers.PositionHandler.position_view(request, position_id)

    else:
        return render(request, 'jobs/403.html')

def position_apply(request, position_id):
    if handlers.AuthHandler.access_granted(request, 'candidate'):
        return handlers.PositionHandler.position_apply(request, position_id)

    else:
        return render(request, 'jobs/403.html')

def position_edit(request, position_id):
    if handlers.AuthHandler.access_granted(request, 'company'):
        return handlers.PositionHandler.position_edit(request, position_id)

    else:
        return render(request, 'jobs/403.html')

def position_confirm_delete(request, position_id):
    if handlers.AuthHandler.access_granted(request, 'company'):
        return handlers.PositionHandler.position_confirm_delete(request, position_id)

    else:
        return render(request, 'jobs/403.html')

def position_delete(request, position_id):
    if handlers.AuthHandler.access_granted(request, 'company'):
        return handlers.PositionHandler.position_delete(request, position_id)

    else:
        return render(request, 'jobs/403.html')

def application_view(request, application_id):
    if handlers.AuthHandler.access_granted(request, ['company', 'candidate']):
        return handlers.ApplicationHandler.application_view(request, application_id)

    else:
        return render(request, 'jobs/403.html')


