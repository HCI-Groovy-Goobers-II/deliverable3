from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Column
from .models import *

class SelectFieldChoices:
    # Create tuples for select option here.
    # The first string in each row is the
    # actual value to store in the database.
    # The second string is what the user sees.

    GRADE_LEVEL_CHOICES = (
        ('Freshman', 'Freshman'),
        ('Sophomore', 'Sophomore'),
        ('Junior', 'Junior'),
        ('Senior', 'Senior'),
        ('Other', 'Other')
    )

# TODO: Finish the student form. Look at the professor form for an example.

class StudentForm(forms.ModelForm):

    profile_icon = forms.FileField(
        label='Profile icon',
        required=False,
        widget=forms.FileInput(attrs={
            'multiple': False,
            'accept': 'image/*'
        })
    )

    grade_level = forms.CharField(
        label='Choose grade level',
        required=True,
        widget=forms.Select(choices=SelectFieldChoices.GRADE_LEVEL_CHOICES)
    )

    pronouns = forms.CharField(
        label='Personal pronouns',
        required=False,
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
        model = Student
        fields = [
            'profile_icon', 'pronouns',
            'bio',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-25 fs-400 ff-sans-normal'
        self.helper.field_class='col-75'
        self.helper.form_tag = False
