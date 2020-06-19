from django.shortcuts import render
from . import auth
from .. import models, utils


def get_positions_listing_context():
    return {'positions': models.JobPosition.objects.all()}


def get_curr_candidate_applications(request):
    return models.Application.objects.filter(candidate=auth.AuthHandler.get_curr_profile(request))


class CandidateHandler():
    def dash(request):
        curr_profile_applications = get_curr_candidate_applications(request)
        context = get_positions_listing_context()
        context['candidate_applications'] = {
            application.position.id for application in curr_profile_applications
        }
        return render(request, 'jobs/candidate_dash.html', context)
