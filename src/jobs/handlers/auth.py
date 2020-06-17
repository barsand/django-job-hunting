from .. import models, utils
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate

class AuthHandler():
    def register_user(request):
        if request.method == 'GET':
            context = {
                'choices': [
                    ('role', 'Tipo de perfil', models.ROLE_CHOICES)
                ]
            }
            return render(request, 'jobs/register.html', context)
        elif request.method == 'POST':
            user_form_data = utils.parse_model_form_data(request, models.User)
            user = models.User.objects.create_user(**user_form_data)
            user.save()

            profile_form_data = utils.parse_model_form_data(request, models.Profile)
            profile = models.Profile(user=user, **profile_form_data)
            profile.save()

            context = {
                'message': {
                    'type': 'success',
                    'text': 'Sua conta foi criada com sucesso!'
                }
            }

            return render(request, 'jobs/register.html', context)

    def login(request):
        if request.method == 'GET':
            return render(request, 'jobs/login.html')
        elif request.method == 'POST':
            form_data = utils.parse_model_form_data(request, models.User)
            user = authenticate(**form_data)
            curr_profile = models.Profile.objects.get(user=user)

            if curr_profile.role in ['company', 'candidate']:
                return redirect('/%s/' % curr_profile.role)

            import ipdb; ipdb.set_trace()
