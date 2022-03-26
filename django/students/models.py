from email.policy import default
from django.db import models
from institutions.models import Institution
from users.models import EmailAuthUser

class StudentRole(models.Model):
    text = models.CharField(max_length=50)

class StudentSkill(models.Model):
    text = models.CharField(max_length=50)

class Student(models.Model):
    pronouns   = models.CharField(max_length=100)
    bio        = models.CharField(max_length=300)
    avg_rating = models.FloatField(default=0)

    avg_participation     = models.FloatField(default=0)
    avg_contribution      = models.FloatField(default=0)
    avg_work_timeliness   = models.FloatField(default=0)
    avg_work_quality      = models.FloatField(default=0)
    avg_cooperativeness   = models.FloatField(default=0)
    avg_communicativeness = models.FloatField(default=0)

    institution = models.ForeignKey(Institution, on_delete=models.DO_NOTHING)
    roles = models.ManyToManyField(StudentRole)
    skills = models.ManyToManyField(StudentSkill)
    user = models.ForeignKey(EmailAuthUser, on_delete=models.CASCADE)