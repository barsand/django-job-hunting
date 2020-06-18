from django.db.models import Q
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

    def position_apply(request, position_id):
        def handle_duplicate():
            context = {
                'message': {
                    'type': 'warning',
                    'text': 'Você já se candidatou a esta vaga!'
                }
            }
            return render(request, 'jobs/position_apply.html', context)
        curr_profile = auth.AuthHandler.get_curr_profile(request)
        curr_position = models.JobPosition.objects.get(id=position_id)
        res = models.Application.objects.filter(
                Q(position=curr_position) & Q(candidate=curr_profile))
        if len(res):
            return handle_duplicate()

        if request.method == 'GET':
            context = {
                'profile': auth.AuthHandler.get_curr_profile(request),
                'position': models.JobPosition.objects.get(id=position_id),
                'choices': [
                    ('education', 'Última escolaridade', models.EDUCATION_CHOICES),
                ]
            }
            return render(request, 'jobs/position_apply.html', context)
        elif request.method == 'POST':
            if not len(res):
                form_data = utils.parse_model_form_data(request, models.Application)
                form_data['candidate'] = curr_profile
                form_data['position'] = curr_position
                application = models.Application(**form_data)
                application.save()
                context = {
                    'message': {
                        'type': 'success',
                        'text': 'Candidatura à vaga "%s" submetida com sucesso!' % form_data['position'].title
                    }
                }
                return render(request, 'jobs/position_apply.html', context)
            else:
                return handle_duplicate()
