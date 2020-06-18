from django.shortcuts import render
from . import auth
from .position import get_profile_positions
from .. import models, utils
import collections

def get_all_positions():
    return {'positions': models.JobPosition.objects.all()}

def get_company_applications(request):
    return models.Application.objects.filter(
            position__publisher__exact=auth.AuthHandler.get_curr_profile(request))


class CompanyHandler():
    def dash(request):
        context = get_profile_positions(request)
        applications = collections.defaultdict(lambda: 0)
        for a in get_company_applications(request):
            applications[a.position.id] += 1
        context = {
            'position2applications_count': [
                (p, applications[p.id])
                for p in context['positions']]
        }
        return render(request, 'jobs/company_dash.html', context)


