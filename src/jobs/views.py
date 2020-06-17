from django.http import HttpResponse
from . import models, utils, handlers


def index(request):
    return HttpResponse('<h1>aloha!</h1>')


def register_user(request):
    return handlers.AuthHandler.register_user(request)


def login(request):
    return handlers.AuthHandler.login(request)


def company_dash(request):
    return handlers.CompanyHandler.dash(request)


def position_create(request):
    return handlers.PositionHandler.create(request)
