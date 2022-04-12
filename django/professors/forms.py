from email.policy import default
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Column
from django.http import HttpResponse, HttpResponseRedirect
from os import path
from .models import *
from .form_widgets import DateTimePickerInput

class customMultipleChoiceField(forms.ModelMultipleChoiceField):
    def instance_label(self, course):
        return "%s" % course.code

class SectionMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, section):
        return "%s" % section.section_code

class StudentMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, student):
        return "%s" % (f"<a class=\"student-name\"{student.user.first_name} "
        f"{student.user.last_name}</a> | <a class=\"student-major\">Major: {student.major}</a> | "
        f"<a class=\"student-gradelevel\">Gradelevel: {student.grade_level}</a>")

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


class CourseForm(forms.ModelForm):
    code = forms.CharField(
        label='Class code',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'The class code..',
        })
    )

    description = forms.CharField(
        label='Title',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'The course title..',
        })
    )

    course_sections = forms.CharField(required=False)
    created_course_sections = forms.CharField(required=False)
    course_sections_to_delete = forms.CharField(required=False)
    created_course_section_ids = forms.CharField(required=False)

    class Meta:
        model = Course
        fields = [
            'code','description',
        ]


class ProjectForm(forms.ModelForm):
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

    start_date = forms.DateTimeField(
        label='Start Date',
        required=True,
        widget=DateTimePickerInput()
    )

    end_date = forms.DateTimeField(
        label='End Date',
        required=True,
        widget=DateTimePickerInput()
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

class ChooseProjectSectionsForm(forms.Form):
    sections = SectionMultipleChoiceField(
        label='Select one or more sections',
        queryset=None,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-25 fs-400 ff-sans-normal'
        self.helper.field_class='col-75'
        self.helper.form_tag = False

        self.course = kwargs.pop('course')
        super().__init__(*args, **kwargs)
        self.fields['sections'].queryset = Section.objects.filter(course=self.course)


class AddSectionForm(forms.ModelForm):
    section_choice = forms.CharField(
        label='Pre-existing Sections',
    )

    class Meta:
        model = Section
        fields = [ 'section_choice' ]

    def __init__(self, *args, **kwargs):
        course = kwargs.pop('course')
        self.choices = [ (s, s) for s in Section.objects.filter(course=course)._clone().values_list('section_code', flat=True) ]

        super().__init__(*args, **kwargs)
        self.fields['section_choice'].widget=forms.Select(
            choices=self.choices
        )
        self.helper = FormHelper()
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-25'
        self.helper.field_class='col-75'
        self.helper.form_tag = False


class ChooseStudentsForm(forms.Form):
    students = StudentMultipleChoiceField(
        label='Select one or more sections',
        queryset=None,
        required=False,
        widget=forms.RadioSelect()
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-25 fs-400 ff-sans-normal'
        self.helper.field_class='col-75'
        self.helper.form_tag = False

        self.institution = kwargs.pop('institution')
        super().__init__(*args, **kwargs)
        self.fields['students'].queryset = Student.objects.filter(institution=self.institution)


class SectionForm(forms.ModelForm):
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

    class Meta:
        model = Section
        fields = [
            'section_code', 'description',
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
                Column('section_code')
            ),
            Row(
                Column('description')
            )
        )