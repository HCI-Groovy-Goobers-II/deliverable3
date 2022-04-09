from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from professors.forms import ProfessorForm, CreateCourseForm, CreateProjectForm, CreateSectionForm
from users.decorators import allowed_users
from professors.models import Professor, Course, Project, Section, S3ProfessorUpload
from students.models import Student
from datetime import datetime as dt, timedelta
from os import path



#region Index Request Return
@login_required
@allowed_users(allowed_groups=['professors'])
def index(request):
    context = {


    }
    return render(request, 'professors/index.html', context)
#endregion

<<<<<<< Updated upstream

#region Debug Request Return
@login_required
@allowed_users(allowed_groups=['professors'])
def debug(request):
    courses = Course.objects.all()
    projects = Project.objects.all()
    sections = Section.objects.all()
    students = Student.objects.all()
    context = {

        'courses': courses,
        'project': projects,
        'section': sections,
        'student': students


=======

#region Debug Request Return
@login_required
@allowed_users(allowed_groups=['professors'])
def debug(request):
    courses = Course.objects.all()
    projects = Project.objects.all()
    sections = Section.objects.all()
    students = Student.objects.all()
    context = {

        'courses': courses,
        'projects': projects,
        'sections': sections,
        'students': students


>>>>>>> Stashed changes
    }
    return render(request, 'professors/debug.html', context)
#endregion



#region Form Views

#region edit_profile (Edit a Professor's profile)
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
#endregion



#region create_course (Form to create a course)
@login_required
@allowed_users(allowed_groups=['professors'])
def create_course(request): 
    professor = Professor.objects.get(user=request.user) #get the current professor
    course = Course(professor=professor) #create a course and specify that the professor value of the course will be set = to the professor

    if request.method != 'POST':  
        form = CreateCourseForm(instance=course)  #Create the form instance of the course
        instance=course # ?
                                               
    else:                                       
        form = CreateCourseForm(instance=course, data=request.POST) #Create the form, instance of the course with a DR post 
        if form.is_valid():
            form.save() #If the form is valid, save it.
        course.save()

        return HttpResponseRedirect(reverse('professors:index')) #Return to the index

    context = { 'form': form }
    return render(request, 'professors/create_course_form.html', context)
#endregion

#region create_project (Form to create a project)
@login_required
@allowed_users(allowed_groups=['professors'])
def create_project(request):
<<<<<<< Updated upstream
    professor = Professor.objects.get(user=request.user)
    course = Course.objects.get(professor=professor)
    project = Project(course=course)
    if request.method != 'POST':
        form = CreateProjectForm() 

    else:                                  
        form = CreateProjectForm(data=request.POST) 
=======
    project = Project()
    if request.method != 'POST':
        form = CreateProjectForm(instance=project, request=request) 

    else:                                  
        form = CreateProjectForm(instance=project, request=request, data=request.POST) 
>>>>>>> Stashed changes
        if form.is_valid():
            form.save()
        project.save()
         
        return HttpResponseRedirect(reverse('professors:index'))

    context = { 'form': form }
    return render(request, 'professors/create_project_form.html', context)
#endregion

#region create_section (Form to create a section)
@login_required
@allowed_users(allowed_groups=['professors'])
def create_section(request):
<<<<<<< Updated upstream

    if request.method != 'POST':
        form = CreateSectionForm() 

    else:                                       
        form = CreateSectionForm(data=request.POST) 
=======
    section = Section()
    if request.method != 'POST':
        form = CreateSectionForm(instance=section, request=request)

    else:                                       
        form = CreateSectionForm(request=request, data=request.POST) 
>>>>>>> Stashed changes
        if form.is_valid():
            form.save()
             
        return HttpResponseRedirect(reverse('professors:index'))

    context = { 'form': form }
    return render(request, 'professors/create_section_form.html', context)
#endregion

<<<<<<< Updated upstream

#endregion
=======
@login_required
@allowed_users(allowed_groups=['professors'])
def index(request):
    professor = Professor.objects.get(user=request.user)
    course = Course.objects.all()
    context = {
        'course' : course,
        'courses' : Course.objects.filter(professor=professor),

    }
    return render(request, 'professors/index.html', context)





>>>>>>> Stashed changes
