from django.shortcuts import render
from . import auth
from .. import models, utils
import collections

class PositionHandler():
    def create(request):
        if request.method == 'GET':
            context = {
                'positions': models.JobPosition.objects.all(),
                'choices': [
                    ('min_education', 'Escolaridade mínima', models.EDUCATION_CHOICES),
                    ('salary', 'Faixa salarial', models.SALARY_CHOICES)
                ]
            }
            return render(request, 'jobs/position_create.html', context)
        elif request.method == 'POST':
            form_data = utils.parse_model_form_data(request, models.JobPosition)
            form_data['publisher'] = auth.AuthHandler.get_curr_profile(request)
            db_job_position = models.JobPosition(**form_data)
            db_job_position.save()
            context = get_profile_positions(request)
            context['message'] = {
                'type': 'success',
                'text': 'Vaga "%s" criada com sucesso!' % db_job_position.title
            }
            return render(request, 'jobs/company_dash.html', context)


    def position_view(request, position_id):
        if request.method == 'GET':
            context = {
                'profile': auth.AuthHandler.get_curr_profile(request),
                'position': models.JobPosition.objects.get(id=position_id)
            }
            return render(request, 'jobs/position_view.html', context)
