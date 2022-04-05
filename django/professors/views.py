from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from professors.forms import ProfessorForm, CreateCourseForm, CreateProjectForm, CreateSectionForm
from users.decorators import allowed_users
from professors.models import Professor, S3ProfessorUpload
from students.models import Student
from datetime import datetime as dt, timedelta
from os import path


#region Routes Request-Returns

#region Index Request Return
@login_required
@allowed_users(allowed_groups=['professors'])
def index(request):
    context = {

    }
    return render(request, 'professors/index.html', context)
#endregion

#region Create Course Request Return
@login_required
@allowed_users(allowed_groups=['professors'])
def controls(request):
    context = {

    }
    return render(request, 'professors/create_course.html', context)
#endregion

#region Create Project Request Return
@login_required
@allowed_users(allowed_groups=['professors'])
def controls(request):
    context = {

    }
    return render(request, 'professors/create_project.html', context)
#endregion

#region Create Project Request Return
@login_required
@allowed_users(allowed_groups=['professors'])
def controls(request):
    context = {

    }
    return render(request, 'professors/create_section.html', context)
#endregion

#endregion

#region Forms Request-Returns

#region ProfessorForm Request Return
@login_required
@allowed_users(allowed_groups=['professors'])
def edit_profile(request):
    professor = Professor.objects.get(user=request.user) #Get  the current professor

    if request.method != 'POST': #If the request method IS NOT a POST
        form = ProfessorForm(instance=professor) #Form is set equal to the ProfessorForm with an instance of the 
                                                # specified professor
    else:                                       #OTHERWISE
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
#endregion

#region CreateCourse Request Return
@login_required
@allowed_users(allowed_groups=['professors'])
def create_course(request):
    professor = Professor.objects.get(user=request.user) #Get  the current professor

    if request.method != 'POST': #If the request method IS NOT a POST
        form = CreateCourseForm() #Form is set equal to the ProfessorForm with an instance of the 
                                                # specified professor
    else:                                       #OTHERWISE
        form = CreateCourseForm(instance=professor, data=request.POST) 
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('professors:create_class'))

    context = { 'form': form }
    return render(request, 'professors/create_class.html', context)
#endregion

#region CreateProject Request Return
@login_required
@allowed_users(allowed_groups=['professors'])
def create_project(request):
    professor = Professor.objects.get(user=request.user)

    if request.method != 'POST':
        form = CreateProjectForm() 
                                                
        form = CreateProjectForm(instance=professor, data=request.POST) 
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('professors:create_project'))

    context = { 'form': form }
    return render(request, 'professors/create_project.html', context)
#endregion

#region CreateSection Request Return
@login_required
@allowed_users(allowed_groups=['professors'])
def create_section(request):
    professor = Professor.objects.get(user=request.user)

    if request.method != 'POST':
        form = CreateSectionForm() 
                                                
        form = CreateSectionForm(instance=professor, data=request.POST) 
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('professors:create_section'))

    context = { 'form': form }
    return render(request, 'professors/create_section.html', context)
#endregion


#endregion