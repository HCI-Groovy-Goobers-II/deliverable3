from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from students.models import *

from users.decorators import allowed_users

from datetime import datetime as dt, timedelta

@login_required
@allowed_users(allowed_groups=['students'])
def index(request):
    student = Student.objects.get(user=request.user)
    context = {
        'student': student,
        'students': Student.objects.filter(institution=student.institution)
    }
    return render(request, 'students/index.html', context)
