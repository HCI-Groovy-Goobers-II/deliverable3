from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Column
from django.http import HttpResponse, HttpResponseRedirect
from os import path
from .models import *

class customMultipleChoiceField(forms.ModelMultipleChoiceField):
    def instance_label(self, course):
        return "%s" % course.code


class ProfessorForm(forms.ModelForm):
    profile_icon = forms.FileField(
        label='Profile icon',
        required=False,
        widget=forms.FileInput(attrs={
            'multiple': False,
            'accept': 'image/*'
        })
    )

    title = forms.CharField(
        label='Professional title',
        required=True,
    )

    pronouns = forms.CharField(
        label='Personal pronouns',
        required=False,
    )

    suffix = forms.CharField(
        label='Your suffix',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'PhD, MD, PhD-MD, etc.'
        })
    )

    bio = forms.CharField(
        label='Bio',
        required=False,
        widget=forms.Textarea(attrs={
            'rows': '3',
            'cols': '40',
            'placeholder': 'Tell students about yourself in 300 characters.'
        })
    )

    class Meta:
        model = Professor
        fields = [
            'profile_icon', 'title', 'pronouns',
            'suffix', 'bio',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-25 fs-400 ff-sans-normal'
        self.helper.field_class='col-75'
        self.helper.form_tag = False


class CreateCourseForm(forms.ModelForm):
    code = forms.CharField(
        label='Class code',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'The class code..',
        })
    )

    description = forms.CharField(
        label='Description',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'The description..',
        })    
    )

    course_sections = forms.CharField()
    
    class Meta:
        model = Course
        fields = [
            'code','description','professor',
        ]


class CreateProjectForm(forms.ModelForm):
    title = forms.CharField(
        label='Project Title',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'The title of the Project..',
        })
    )

    description = forms.CharField(
        label='Description',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'The description..',
        })
    )

    start_date = forms.CharField(
        label='Start Date',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'The start date..',
        })
    )


    end_date = forms.CharField(
        label='End Date',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'The end date..',
        })              
    
    )
    course = forms.ModelChoiceField(
        label='Course',
        queryset=None,
        required = True
    )

    class Meta:
        model = Project
        fields = [
            'title', 'description', 'start_date', 'end_date', 'course',
        ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')        
        super().__init__(*args, **kwargs)

        professor = Professor.objects.get(user=self.request.user)        
        self.fields['course'].queryset = Course.objects.filter(professor=professor)

        self.helper = FormHelper()
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-25 fs-400 ff-sans-normal'
        self.helper.field_class='col-75'
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('title')
            ),
            Row(
                Column('description')
            ),
            Row(
                Column('start_date')
            ),
            Row(
                Column('end_date')
            ),
            Row(
                Column('course')
            ),                          
        )


class CreateSectionForm(forms.ModelForm):
    section_code = forms.CharField(
        label='Section Code',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'The code of the section..',
        })
    )

    description = forms.CharField(
        label='Description',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'The description of the section..',
        })
    )

    course = forms.CharField(
        label='Course',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'The course of the section..',
        })
    )    

    projects = forms.CharField(
        label='Projects',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'The projects of the section..',
        })
    )    


    students = forms.CharField(
        label='Students',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'The students of the section..',
        })
    )    

    class Meta:
        model = Section
        fields = [
            'section_code', 'description', 'course', 'projects', 'students',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-25 fs-400 ff-sans-normal'
        self.helper.field_class='col-75'
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('title')
            ),
            Row(
                Column('description')
            ),
            Row(
                Column('course')
            ),
            Row(
                Column('projects')
            ),
            Row(
                Column('students')
            ),                          
        )