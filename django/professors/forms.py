from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Column
from .models import *

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
        self.helper.label_class='col-25'
        self.helper.field_class='col-75'
        self.helper.form_tag = False