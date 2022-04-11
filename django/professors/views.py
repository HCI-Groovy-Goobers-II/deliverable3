from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from professors.forms import *
from users.decorators import allowed_users
from professors.models import *
from students.models import Student
from datetime import datetime as dt, timedelta
from django.contrib import messages
from os import path


@login_required
@allowed_users(allowed_groups=['professors'])
def index(request):
    professor = Professor.objects.get(user=request.user)
    courses = Course.objects.filter(professor=professor)
    sections = set()
    projects = set()
    for _, c in enumerate(courses):
        projects = projects.union(Project.objects.filter(course=c))
        sections = sections.union(Section.objects.filter(course=c))

    context = {
        'courses' : Course.objects.filter(professor=professor),
        'sections': sections,
        'projects': projects
    }
    return render(request, 'professors/index.html', context)


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
    }
    return render(request, 'professors/debug.html', context)


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

    context = { 'professor': professor, 'form': form }
    return render(request, 'professors/edit_profile_form.html', context)


@login_required
@allowed_users(allowed_groups=['professors'])
def create_course(request): 
    professor = Professor.objects.get(user=request.user) #get the current professor
    course = Course(professor=professor) #create a course and specify that the professor value of the course will be set = to the professor

    if request.method != 'POST':  
        form = CreateCourseForm(instance=course)  #Create the form instance of the course
    else:
        print("POST")
        form = CreateCourseForm(instance=course, data=request.POST) #Create the form, instance of the course with a DR post 
        if form.is_valid():
            form.save() #If the form is valid, save it.
            sections_str = request.POST['course_sections'].split('|')
            for sc in sections_str: # Build the sections
                section = Section(
                    section_code=sc,
                    description='',
                    course=course
                )
                section.save()
            return HttpResponseRedirect(reverse('professors:index')) #Return to the index
        else:
            if request.POST['course_sections'] == '':
                form.add_error('course_sections', 'You must create at least one section');

    context = { 'form': form }
    return render(request, 'professors/create_course_form.html', context)


@login_required
@allowed_users(allowed_groups=['professors'])
def create_project(request):
    project = Project()
    courses = Course.objects.filter(professor=Professor.objects.get(user=request.user))
    #sections = set()
    #for course in courses:
    #    sections = sections.union(Section.objects.filter(course=course)) # Get all candidate sections

    if request.method != 'POST':
        form = CreateProjectForm(instance=project, request=request) 

    else:                                  
        form = CreateProjectForm(instance=project, request=request, data=request.POST) 
        if form.is_valid():
            form.save()
        project.save()
         
        return HttpResponseRedirect(reverse('professors:index'))

    context = { 'form': form }
    return render(request, 'professors/create_project_form.html', context)


@login_required
@allowed_users(allowed_groups=['professors'])
def create_section(request):
    section = Section()
    if request.method != 'POST':
        form = CreateSectionForm(instance=section)
    else:                                       
        form = CreateSectionForm(request=request, data=request.POST) 
        if form.is_valid():
            form.save()
             
        return HttpResponseRedirect(reverse('professors:index'))

    context = {
        'form': form,
        'dont_display': True
    }
    return render(request, 'professors/create_section_form.html', context)





