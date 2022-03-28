from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from professors.forms import ProfessorForm

from users.decorators import allowed_users
from professors.models import Professor, S3ProfessorUpload
from students.models import Student

from datetime import datetime as dt, timedelta
from os import path

@login_required
@allowed_users(allowed_groups=['professors'])
def index(request):
    context = {

    }
    return render(request, 'professors/index.html', context)

@login_required
@allowed_users(allowed_groups=['professors'])
def edit_profile(request):
    professor = Professor.objects.get(user=request.user)

    if request.method != 'POST':
        form = ProfessorForm(instance=professor)
    else:
        form = ProfessorForm(instance=professor, data=request.POST)
        if form.is_valid():
            form.save()
            if len(request.FILES) != 0:
                if 'profile_icon' in request.FILES.keys():
                    image = request.FILES['profile_icon']
                    image.name = 'profile-icon-' + str(professor.id) + path.splitext(image.name)[1]
                    u = S3ProfessorUpload(file=image)
                    u.save()
                    professor.profile_icon_file_name=image.name
                    professor.save()

            return HttpResponseRedirect(reverse('professors:index'))

    context = { 'form': form }
    return render(request, 'professors/edit_profile_form.html', context)
