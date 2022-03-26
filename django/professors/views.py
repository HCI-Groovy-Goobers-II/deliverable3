from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

from users.decorators import allowed_users
from students.models import Student
from professors.models import Professor

from datetime import datetime as dt, timedelta

@login_required
@allowed_users(allowed_groups=['professors'])
def index(request):
    prof = Professor.objects.get(user=request.user)
    students = Student.objects.filter(institution=prof.institution)
    context = {
        'professor': prof,
        'students': students
    }
    return render(request, 'professors/index.html', context)
