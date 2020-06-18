from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('company/position_create/', views.position_create, name='position_create')
]
