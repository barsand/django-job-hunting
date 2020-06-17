from django.db import models

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

class JobPosition(models.Model):
    title = models.CharField(max_length=100)
    salary = models.CharField(max_length=16, choices=SALARY_CHOICES)
    requirements = models.CharField(max_length=1000)
    min_education = models.CharField(max_length=20, choices=EDUCATION_CHOICES)

