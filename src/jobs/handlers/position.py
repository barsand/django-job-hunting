from django.shortcuts import render
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


