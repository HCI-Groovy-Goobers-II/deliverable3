from email.policy import default
from django.db import models
from institutions.models import Institution
from users.models import EmailAuthUser
from functools import partial
from os import path

'''
I've already added the profile_image and profile_image_file_name
fields to the Student model and got the upload models and the Student
models migrated. It's up to you to implement it by writing the views
code, the form, the urls routing, and the HTML template.
'''

def _update_filename(instance, filename, path):
    return path.join(path, filename)

def upload_to(path):
    return partial(_update_filename, path=path)

class S3Upload(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)

class S3StudentUpload(S3Upload):
    _upload_to='img/students/profile_icons'
    file = models.FileField(upload_to=(_upload_to))

class StudentRole(models.Model):
    text = models.CharField(max_length=50)

class StudentSkill(models.Model):
    text = models.CharField(max_length=50)

class Student(models.Model):
    pronouns    = models.CharField(max_length=100)
    bio         = models.CharField(max_length=300)
    grade_level = models.CharField(max_length=9)
    major       = models.CharField(max_length=69)
    minor       = models.CharField(max_length=69)
    avg_rating  = models.FloatField(default=0)

    avg_participation     = models.FloatField(default=0)
    avg_contribution      = models.FloatField(default=0)
    avg_work_timeliness   = models.FloatField(default=0)
    avg_work_quality      = models.FloatField(default=0)
    avg_cooperativeness   = models.FloatField(default=0)
    avg_communicativeness = models.FloatField(default=0)

    profile_icon           = models.FileField()
    profile_icon_file_name = models.CharField(max_length=30, default='default_profile_icon.png')

    institution = models.ForeignKey(Institution, on_delete=models.DO_NOTHING)
    roles = models.ManyToManyField(StudentRole)
    skills = models.ManyToManyField(StudentSkill)
    user = models.ForeignKey(EmailAuthUser, on_delete=models.CASCADE)

    def __str__(self):
        return (
            f"\nid:        {self.id}\n"
            f"institution: {self.institution}\n"
            f"profile icon path:      '{S3StudentUpload._upload_to}'\n"
            f"profile icon file name: '{self.profile_icon_file_name}'"
        )