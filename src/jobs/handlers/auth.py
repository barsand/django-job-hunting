from .. import models, utils
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


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
            login(request, user)

            curr_profile = models.Profile.objects.get(user=user)

            return redirect('/home/')

    def get_curr_profile(request):
        try:
            return models.Profile.objects.get(user=request.user)
        except:
            return None

    def access_granted(request, allowed_roles):
        if isinstance(allowed_roles, str):
            allowed_roles = [allowed_roles]
        try:
            assert request.user.is_authenticated
            profile = models.Profile.objects.get(user=request.user)
            assert profile is not None
            assert profile.role in allowed_roles
            return True
        except AssertionError as exp:
            return False


