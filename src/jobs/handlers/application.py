from django.shortcuts import render
from . import auth
from .. import models, utils
import collections

def get_application(application_id):
    return models.Application.objects.get(id=application_id)


class ApplicationHandler():
    def application_view(request, application_id):
        if request.method == 'GET':
            context = {'application': get_application(application_id)}
            return render(request, 'jobs/application_view.html', context)

