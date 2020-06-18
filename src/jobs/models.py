from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save


EDUCATION_CHOICES = [
    ('EF', 'Ensino fundamental'),
    ('EM', 'Ensino médio'),
    ('TEC', 'Tecnólogo'),
    ('ES', 'Ensino Superior'),
    ('POS', 'Pós / MBA / Mestrado'),
    ('PHD', 'Doutorado')
]

SALARY_CHOICES = [
    ('0-1', 'Até 1.000'),
    ('1-2', 'De 1.000 a 2.000'),
    ('2-3', 'De 2.000 a 3.000'),
    ('3+', 'Acima de 3.000')
]

ROLE_CHOICES = [
    ('company', 'Empresa'),
    ('candidate', 'Candidato'),
]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.TextField(max_length=300)
    role = models.TextField(max_length=10, choices=ROLE_CHOICES)


class JobPosition(models.Model):
    title = models.CharField(max_length=100)
    salary = models.CharField(max_length=16, choices=SALARY_CHOICES)
    requirements = models.CharField(max_length=1000)
    min_education = models.CharField(max_length=20, choices=EDUCATION_CHOICES)
    publisher = models.ForeignKey(Profile, on_delete=models.CASCADE)

class Application(models.Model):
    position = models.ForeignKey(JobPosition, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Profile, on_delete=models.CASCADE)
    salary_claim = models.IntegerField()
    professional_experience = models.CharField(max_length=1000)
    education = models.CharField(max_length=20, choices=EDUCATION_CHOICES)
