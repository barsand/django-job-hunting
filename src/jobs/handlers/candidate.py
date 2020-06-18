from django.shortcuts import render
from . import auth
from .. import models, utils

def get_positions_listing_context():
    return {'positions': models.JobPosition.objects.all()}

class CandidateHandler():
    def dash(request):
        context = get_positions_listing_context()
        return render(request, 'jobs/candidate_dash.html', context)

    def position_view(request, position_id):
        if request.method == 'GET':
            context = {
                'profile': auth.AuthHandler.get_curr_profile(request),
                'position': models.JobPosition.objects.get(id=position_id)
            }
            return render(request, 'jobs/position_view.html', context)

    def position_apply(request, position_id):
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
            form_data = utils.parse_model_form_data(request, models.Application)
            form_data['candidate'] = auth.AuthHandler.get_curr_profile(request)
            form_data['position'] = models.JobPosition.objects.get(id=position_id)
            application = models.Application(**form_data)
            Application.save()

            import ipdb; ipdb.set_trace()
