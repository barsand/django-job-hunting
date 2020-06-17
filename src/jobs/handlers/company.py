from django.shortcuts import render
from .. import models, utils

def get_positions_listing_context():
    return {'positions': models.JobPosition.objects.all()}

class CompanyHandler():
    def dash(request):
        context = get_positions_listing_context()
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
            db_job_position = models.JobPosition(**form_data)
            db_job_position.save()
            context = get_positions_listing_context()
            context['message'] = {
                'type': 'success',
                'text': 'Vaga "%s" criada com sucesso!' % db_job_position.title
            }
            return render(request, 'jobs/company_dash.html', context)

