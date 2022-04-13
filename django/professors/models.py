from pyexpat import model
from django.db import models
from institutions.models import Institution
from users.models import EmailAuthUser
from students.models import Student

from functools import partial
from os import path


def _update_filename(instance, filename, path):
    return path.join(path, filename)

def upload_to(path):
    return partial(_update_filename, path=path)


class S3Upload(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)


class S3ProfessorUpload(S3Upload):
    _upload_to='img/professors/profile_icons'
    file = models.FileField(upload_to=(_upload_to))


class Professor(models.Model):
    title        = models.CharField(max_length=100)
    pronouns     = models.CharField(max_length=100)
    suffix       = models.CharField(max_length=10)
    bio          = models.CharField(max_length=300)

    profile_icon           = models.FileField()
    profile_icon_file_name = models.CharField(max_length=30, default='default_profile_icon.png')

    institution = models.ForeignKey(Institution, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(EmailAuthUser, on_delete=models.CASCADE)

    def __str__(self):
        return (
            f"\nid:         {self.id}\n"
            f"title:       {self.title}\n"
            f"institution: {self.institution}\n"
            f"profile icon path:      '{S3ProfessorUpload._upload_to}'\n"
            f"profile icon file name: '{self.profile_icon_file_name}'"
        )

    def print_userfriendly(self):
        return(
            f"{self.user.last_name}\n"
        )


class Course(models.Model):
    code = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)

    def __str__(self):
        return (
            f"\n{self.code}: {self.description}"
            f", {self.professor.user.last_name}"
        )


class Project(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return (
            f"\ntitle:      {self.title}\n"
            f"description: {self.description}\n"
            f"course:      {self.course.code}\n"
        )


class Section(models.Model):
    section_code = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    projects = models.ManyToManyField(Project)
    students = models.ManyToManyField(Student)
    
        

    


