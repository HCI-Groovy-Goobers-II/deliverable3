from django.db import models
from institutions.models import Institution
from users.models import EmailAuthUser


class Professor(models.Model):
    title    = models.CharField(max_length=100)
    pronouns = models.CharField(max_length=100)
    suffix   = models.CharField(max_length=10)
    bio      = models.CharField(max_length=300)

    institution = models.ForeignKey(Institution, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(EmailAuthUser, on_delete=models.CASCADE)
