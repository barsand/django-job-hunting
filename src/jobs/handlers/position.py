from django.shortcuts import render
from django.db.models import Q
from . import auth
from .. import models, utils
import collections


def get_profile_positions(request):
    curr_profile = auth.AuthHandler.get_curr_profile(request)
    return {'positions': models.JobPosition.objects.filter(publisher=curr_profile)}

def get_position_applications(position):
    return models.Application.objects.filter(position=position)

def get_position(request, position_id):
    try:
        curr_profile = auth.AuthHandler.get_curr_profile(request)
        return models.JobPosition.objects.get(id=position_id,
                                              publisher=curr_profile)
    except Exception as exp:
        return None

def calculate_score(application_form):
    score = 0

    claim_range = 0
    salary_claim = int(application_form['salary_claim'])
    if  salary_claim > 1000:
        claim_range += 1
    if  salary_claim > 2000:
        claim_range += 1
    if  salary_claim > 3000:
        claim_range += 1

    salary_levels = [i[0] for i in models.SALARY_CHOICES]
    position_salary_range = salary_levels.index(application_form['position'].salary)

    if salary_levels[claim_range] == application_form['position'].salary:
        print('score for salary')
        score += 1

    education_levels = [i[0] for i in models.EDUCATION_CHOICES]
    application_education_level = education_levels.index(application_form['education'])
    min_education_level = education_levels.index(application_form['position'].min_education)
    if application_education_level >= min_education_level:
        print('score for education')
        score += 1

    return score


class PositionHandler():
    def position_create(request):
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
            return render(request, 'jobs/position_create.html', context)


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
                form_data['score'] = calculate_score(form_data)
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

    def position_view(request, position_id):
        if request.method == 'GET':
            curr_profile = auth.AuthHandler.get_curr_profile(request)
            curr_position = models.JobPosition.objects.get(id=position_id)
            context = {
                'profile': curr_profile,
                'position': curr_position
            }
            if curr_profile.role == 'company':
                context['applications'] = get_position_applications(curr_position)
            return render(request, 'jobs/position_view.html', context)

    def position_edit(request, position_id):
        curr_position = get_position(request, position_id)
        if curr_position is None:
            return render(request, 'jobs/403.html')
        context = {
            'position': curr_position,
            'choices': [
                ('min_education', 'Escolaridade mínima', models.EDUCATION_CHOICES),
                ('salary', 'Faixa salarial', models.SALARY_CHOICES)
            ]
        }

        if request.method == 'GET':
            return render(request, 'jobs/position_edit.html', context)
        elif request.method == 'POST':
            form_data = utils.parse_model_form_data(request, models.JobPosition)
            updated_fields = 0
            for field, form_value in form_data.items():
                if str(curr_position.__getattribute__(field)) != form_value:
                    setattr(curr_position, field, form_value)
                    updated_fields += 1
            curr_position.save()

            if updated_fields:
                context['message'] = {
                    'type': 'success',
                    'text': 'Vaga "%s" alterada com sucesso!' % curr_position.title
                }

            return render(request, 'jobs/position_edit.html', context)

    def position_confirm_delete(request, position_id):
        context = {'position': get_position(request, position_id)}
        if request.method == 'GET':
            return render(request, 'jobs/position_confirm_delete.html', context)

    def position_delete(request, position_id):
        if request.method == 'GET':
            curr_position = get_position(request, position_id)
            curr_position.delete()
            context = dict()
            context['message'] = {
                'type': 'success',
                'text': 'Vaga removida!'
            }
            return render(request, 'jobs/position_delete.html', context)


