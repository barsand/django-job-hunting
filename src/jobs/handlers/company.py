from django.shortcuts import render
from . import auth
from .. import models, utils
import collections

def get_all_positions():
    return {'positions': models.JobPosition.objects.all()}

def get_profile_positions(request):
    curr_profile = auth.AuthHandler.get_curr_profile(request)
    return {'positions': models.JobPosition.objects.filter(publisher=curr_profile)}


def get_company_applications(request):
    return models.Application.objects.filter(position__publisher__exact=auth.AuthHandler.get_curr_profile(request))


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

