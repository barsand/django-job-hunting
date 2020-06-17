from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('company/', views.company_dash, name='company_dash'),
    path('company/position_create/', views.position_create, name='position_create')
]
