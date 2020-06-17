from django.http import HttpResponse

from . import models, utils
from .handlers import company


def index(request):
    return HttpResponse('<h1>aloha!</h1>')


def company_dash(request):
    return company.CompanyHandler.dash(request)


def position_create(request):
    return company.PositionHandler.create(request)
