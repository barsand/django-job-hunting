from django.shortcuts import render
from . import auth, position, company
from .. import models, utils
import collections
import json

def get_plot_context(request):
    profile_positions = position.get_profile_positions(request)['positions']
    monthly_position_creation = collections.defaultdict(lambda: 0)

    for p in profile_positions:
        monthly_position_creation[p.created.strftime('%Y-%m')] += 1

    applications_received = company.get_company_applications(request)
    monthly_applications_submission = collections.defaultdict(lambda: 0)

    for a in applications_received:
        monthly_applications_submission[a.created.strftime('%Y-%m')] += 1

    return {
        'plot_data': [
            (
                'positions_per_month',
                'Vagas criadas por mês',
                json.dumps(sorted(
                    [{'t': date, 'y': count} for date, count
                     in monthly_position_creation.items()],
                    key= lambda x: x['t']
                ))
            ),
            (
                'applications_per_month',
                'Candidatos recebidos por mês',
                json.dumps(sorted(
                    [{'t': date, 'y': count} for date, count
                     in monthly_applications_submission.items()],
                    key= lambda x: x['t']
                ))
            )
        ]
    }

class ReportHandler():
    def report_view(request):
        if request.method == 'GET':
            context = get_plot_context(request)
            return render(request, 'jobs/reports.html', context)

