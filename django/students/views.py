from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from students.models import *
from students.forms import *

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

@login_required
@allowed_users(allowed_groups=['students'])
def edit_profile(request):
    student = Student.objects.get(user=request.user) 
    if request.method != 'POST': 
        form = StudentForm(instance=student)
    else:                                       
        form = StudentForm(instance=student, data=request.POST) 
        if form.is_valid():
            print(form.fields['grade_level'])
            form.save()
            print(request.POST['grade_level'])
            if len(request.FILES) != 0:
                if 'profile_icon' in request.FILES.keys():
                    image = request.FILES['profile_icon']
                    image.name = 'profile-icon-' + str(student.id) + path.splitext(image.name)[1]
                    u = S3StudentUpload(file=image)
                    u.save()
                    student.profile_icon_file_name=image.name
                    student.save()

            return HttpResponseRedirect(reverse('students:index'))

    context = { 'student': student, 'form': form }
    return render(request, 'students/edit_profile_form.html', context)

