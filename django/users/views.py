from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from institutions.models import Institution
from professors.models import Professor
from students.models import Student
from .forms import *

User = get_user_model()

@login_required
def route_user(request):
    if request.user.groups.exists():
        is_professor = False; is_student = False
        for group in request.user.groups.all():
            if group.name == 'professors':
                is_professor = True
            if group.name == 'students':
                is_student = True

        if is_professor and is_student:
            return HttpResponseRedirect(reverse('users:choose_app_view'))
        elif is_student:
            return HttpResponseRedirect(reverse('students:index'))
        else:
            return HttpResponseRedirect(reverse('professors:index'))
    else:
        return HttpResponseRedirect(reverse('public_pages:index'))

def login_view(request):
    logout(request)
    if request.method != 'POST':
        form = LoginForm()
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=request.POST['username'],
                                password=request.POST['password'])

            if not (user is None):
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('users:route_user'))

    context = { 'form': form }
    return render(request, 'users/login.html', context)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('public_pages:index'))

def register(request):
    if request.method != 'POST':
        form = EmailAuthUserCreationForm()
    else:
        form = EmailAuthUserCreationForm(data=request.POST)
        formdata = request.POST

        if formdata['password']!=formdata['password_confirm']:
                form.add_error('password_confirm', 'The passwords do not match.')

        if User.objects.filter(email=formdata['email'].lower()).exists():
            form.add_error('email', 'An account with this email address already exists.')

        if form.is_valid():
            email_domain = formdata['email'].split('@')[1]
            institutions = Institution.objects.filter(student_email_domain=email_domain)
            if len(institutions) == 0:
                institutions = Institution.objects.filter(professor_email_domain=email_domain)

            if len(institutions) == 1:
                user = User.objects.create_user(email=formdata['email'], password=formdata['password'])
                user.first_name=formdata['first_name']
                user.last_name=formdata['last_name']

                role_choice = formdata['role_choice']
                professors_group = Group.objects.get(name='professors')
                students_group = Group.objects.get(name='students')

                print("ROLE CHOICE")
                print(role_choice)


                if role_choice == 'both':
                    user.groups.add(professors_group)
                    user.groups.add(students_group)
                    prof = Professor(
                        title='',
                        pronouns='',
                        suffix='',
                        bio='',
                        institution=institutions[0],
                        user=user
                    )
                    prof.save()

                    student = Student(
                        pronouns='',
                        bio='',
                        institution=institutions[0],
                        user=user
                    )
                    student.save()

                elif role_choice == 'students':
                    user.groups.add(students_group)
                    student = Student(
                        pronouns='',
                        bio='',
                        institution=institutions[0],
                        user=user
                    )
                    student.save()
                else:
                    user.groups.add(professors_group)
                    prof = Professor(
                        title='',
                        pronouns='',
                        suffix='',
                        bio='',
                        institution=institutions[0],
                        user=user
                    )
                    prof.save()
                user.save()
            else:
                form.add_error('email', 'Your institution has not registered your email domain.')

            if form.is_valid():
                context = { 'user': user }
                return render(request, 'users/registration_successful.html', context)

    context = { 'form': form }
    return render(request, 'users/register.html', context)

def choose_app_view(request):
    return render(request, 'users/choose_app_view.html', {})