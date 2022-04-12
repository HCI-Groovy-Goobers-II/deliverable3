from xml.etree.ElementInclude import include
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

    context = {
        'courses' : Course.objects.filter(professor=professor),
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

            return HttpResponseRedirect(reverse('professors:manage_courses_and_projects'))

    context = { 'professor': professor, 'form': form }
    return render(request, 'professors/edit_profile_form.html', context)


@login_required
@allowed_users(allowed_groups=['professors'])
def manage_courses_and_projects(request):
    professor = Professor.objects.get(user=request.user)
    courses = Course.objects.filter(professor=professor)

    context = {
        'courses': courses,
        'goto_tab': 'courses'
    }
    return render(request, 'professors/manage_courses_and_projects.html', context)


@login_required
@allowed_users(allowed_groups=['professors'])
def manage_courses_and_projects_tab(request, tab):
    professor = Professor.objects.get(user=request.user)
    courses = Course.objects.filter(professor=professor)

    context = {
        'courses': courses,
        'goto_tab': tab
    }
    return render(request, 'professors/manage_courses_and_projects.html', context)


@login_required
@allowed_users(allowed_groups=['professors'])
def create_course(request): 
    professor = Professor.objects.get(user=request.user) #get the current professor
    course = Course(professor=professor) #create a course and specify that the professor value of the course will be set = to the professor

    if request.method != 'POST':
        form = CourseForm(instance=course)  #Create the form instance of the course
    else:
        form = CourseForm(instance=course, data=request.POST) #Create the form, instance of the course with a DR post
        if len(request.POST['course_sections']) == 0:
            form.add_error('course_sections', 'You must create at least one section')

        if form.is_valid():
            form.save() #If the form is valid, save it.
            sections_str = request.POST['course_sections'].split(';')
            for sc in sections_str: # Build the sections
                if not sc == '':
                    section = Section(
                        section_code=sc,
                        description='',
                        course=course
                    )
                    section.save()
            return HttpResponseRedirect(reverse('professors:manage_courses_and_projects'))

    context = { 'form': form }
    return render(request, 'professors/create_course_form.html', context)


@login_required
@allowed_users(allowed_groups=['professors'])
def edit_course(request, course_id):
    course = Course.objects.get(id=course_id)
    sections = Section.objects.filter(course=course)

    section_ids_str = ""
    section_codes_str = ""

    for section in sections:
        section_ids_str += str(section.id) + ";"
        section_codes_str += section.section_code + ";"

    section_ids_str.rstrip(';')
    section_codes_str.rstrip(';')

    if request.method != 'POST':
        form = CourseForm(instance=course)  #Create the form instance of the course
    else:
        form = CourseForm(instance=course, data=request.POST) #Create the form, instance of the course with a DR post
        if ( (len(request.POST['course_sections']) == 0)
                and (len(request.POST['course_sections_to_delete']) >= len(sections)) ):
            form.add_error('course_sections', 'You must create at least one section')

        elif form.is_valid():
            form.save() #If the form is valid, save it.
            sections_str = request.POST['course_sections_to_delete'].split(';')
            for s_id in sections_str:
                if not s_id == '':
                    section = Section.objects.get(id=int(s_id))
                    section.delete()

            sections_str = request.POST['course_sections'].split(';')
            for sc in sections_str: # Build the sections
                if not sc == '':
                    section = Section(
                        section_code=sc,
                        description='',
                        course=course
                    )
                    section.save()
            return HttpResponseRedirect(reverse('professors:manage_courses_and_projects')) #Return to the index

    context = {
        'form': form,
        'course': course,
        'created_course_sections': section_codes_str,
        'created_course_section_ids': section_ids_str
    }

    return render(request, 'professors/edit_course_form.html', context)


@login_required
@allowed_users(allowed_groups=['professors'])
def choose_project_sections(request, project_id):
    project = Project.objects.get(id=project_id)
    course = Course.objects.get(id=project.course.id)
    sections = Section.objects.filter(course=course) # available sections

    if request.method != 'POST':
        form = ChooseProjectSectionsForm(course=course)
    else:
        form = ChooseProjectSectionsForm(course=course, data=request.POST)
        if form.is_valid():

            print(request.POST['sections'])

            return HttpResponseRedirect(reverse('professors:manage_courses_and_projects', args=['projects']))

    context = {
        'project': project,
        'sections': sections,
        'form': form,
    }

    return render(request, 'professors/choose_project_sections_form.html', context)


@login_required
@allowed_users(allowed_groups=['professors'])
def confirm_delete_course(request, course_id):
    course = Course.objects.get(id=course_id)
    context = {
        'item_id': course.id,
        'item_name': 'Course',
        'item_description': course.code,
        'item_delete_url': 'professors:delete_course'
    }
    return render(request, 'professors/confirm_delete_item.html', context)


@login_required
@allowed_users(allowed_groups=['professors'])
def delete_course(request, course_id):
    course = Course.objects.get(id=course_id)
    course.delete()
    return HttpResponseRedirect(reverse('professors:manage_courses_and_projects'))


@login_required
@allowed_users(allowed_groups=['professors'])
def create_project(request):
    project = Project()

    if request.method != 'POST':
        form = ProjectForm(instance=project, request=request)
    else:                                  
        form = ProjectForm(instance=project, request=request, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('professors:choose_project_sections', args=[project.id]))

    context = { 'project': project, 'form': form }
    return render(request, 'professors/create_project_form.html', context)


@login_required
@allowed_users(allowed_groups=['professors'])
def edit_project(request, project_id):
    project = Project.objects.get(id=project_id)
    if request.method != 'POST':
        form = ProjectForm(instance=project, request=request)
    else:
        form = ProjectForm(instance=project, request=request, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('professors:choose_project_sections', args=[project.id]))

    context = { 'project': project, 'form': form }
    return render(request, 'professors/edit_project_form.html', context)


@login_required
@allowed_users(allowed_groups=['professors'])
def confirm_delete_project(request, project_id):
    project = Project.objects.get(id=project_id)
    context = {
        'item_id': project.id,
        'item_name': 'Project',
        'item_description': project.title,
        'item_delete_url': 'professors:delete_project'
    }
    return render(request, 'professors/confirm_delete_item.html', context)



@login_required
@allowed_users(allowed_groups=['professors'])
def delete_project(request, project_id):
    project = Project.objects.get(id=project_id)
    project.delete()
    return HttpResponseRedirect(reverse('professors:manage_courses_and_projects', args=['projects']))


@login_required
@allowed_users(allowed_groups=['professors'])
def create_section(request, course_id):
    course = Course.objects.get(id=course_id)
    if request.method != 'POST':
        form = SectionForm()
    else:                                       
        form = SectionForm(data=request.POST)
        if form.is_valid():
            sections = Section.objects.filter(course=course)
            pre_existing = sections.filter(section_code=request.POST['section_code'])
            if len(pre_existing) != 0:
                form.add_error('section_code', 'You cannot have two sections with the same code.')
            new_section = form.save(commit=False)
            new_section.course = course

            return HttpResponseRedirect(reverse('professors:manage_courses_and_projects'))

    context = {
        'form': form,
        'course_code': course.code
    }

    return render(request, 'professors/create_section_form.html', context)


@login_required
@allowed_users(allowed_groups=['professors'])
def edit_section(request, section_id):
    section = Section.objects.get(id=section_id)
    if request.method != 'POST':
        form = SectionForm()
    else:
        form = SectionForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('professors:manage_courses_and_projects'))

    context = {
        'form': form,
        'course_code': section.course
    }

    return render(request, 'professors/edit_section_form.html', context)

@login_required
@allowed_users(allowed_groups=['professors'])
def confirm_delete_section(request, section_id):
    section = Section.objects.get(id=section_id)
    context = {
        'item_id': section.id,
        'item_name': 'Section',
        'item_description': section.section_code,
        'item_delete_url': 'professors:delete_section'
    }
    return render(request, 'professors/confirm_delete_item.html', context)


@login_required
@allowed_users(allowed_groups=['professors'])
def delete_section(request, section_id):
    section = Section.objects.get(id=section_id)
    section.delete()
    return HttpResponseRedirect(reverse('professors:manage_courses_and_projects'))




