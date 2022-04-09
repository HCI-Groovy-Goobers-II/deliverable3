from django import forms
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Column
from password_validator import PasswordValidator
from django.contrib.auth.forms import SetPasswordForm

schema1 = PasswordValidator()
schema2 = PasswordValidator()

schema1\
.min(8)\
.max(100)\
.has().uppercase()\
.has().lowercase()\

schema1\
.has().digits()\
.has().no().spaces()


APP_ROLES = (
    ('students', 'Student'),
    ('professors', 'Professor'),
    ('both', 'Both')
)

#region Create an EmailAuthUser
class EmailAuthUserCreationForm(forms.Form):
    first_name = forms.CharField(
        label='First name',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Your first name..',
        })
    )

    last_name = forms.CharField(
        label='Last name',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Your last name..',
        })
    )

    email = forms.EmailField(
        label='School email',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Your college/university email address..',
        })
    )

    password = forms.CharField(
        label='Create password',
        required=True,
        help_text='Must be 8-100 characters including an uppercase and lowercase character and a digit',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter password..',
        })
    )

    password_confirm = forms.CharField(
        label='Re-enter password',
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat the password..'
        })
    )

    role_choice = forms.CharField(
        label='Choose role',
        required=True,
        widget=forms.Select(choices=APP_ROLES)
    )

    tos = forms.BooleanField(
        label='Terms of Service',
        required=True,
    )

    def clean_email(self):
        if EmailAuthUser.objects.filter(email=self.cleaned_data['email'].lower()).exists():
            self.add_error('email', 'An account with this email address already exists.')

    def clean_password(self):
        passwd1 = self.cleaned_data['password']
        passwd2 = self.cleaned_data['password_confirm']

        if passwd1 and passwd2:
            # Check that passwords match
            if passwd1 != passwd2:
                self.add_error('password_confirm', 'The passwords do not match.')

            # Check password requirements
            if len(passwd1) < 8:
                self.add_error('password', "Password must be 8-100 characters")
            if not schema1.validate(passwd1):
                self.add_error('password', "Password must have an uppercase and a lowercase letter")
            if not schema2.validate(passwd1):
                self.add_error('password' "Password must contain a digit and no spaces")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-25 fs-400 ff-sans-normal'
        self.helper.field_class='col-75'
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('first_name')
            ),
            Row(
                Column('last_name')
            ),
            Row(
                Column('email')
            ),
            Row(
                Column('password')
            ),
            Row(
                Column('password_confirm')
            ),
            Row(
                Column('role_choice')
            )
        )
#endregion

class LoginForm(forms.Form):
    username = forms.EmailField(
        label='Email',
        required=True
    )

    password = forms.CharField(
        label='Password',
        required=True,
        widget=forms.PasswordInput()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-25 fs-400 ff-sans-normal'
        self.helper.field_class='col-75'
        self.helper.form_tag = False

class CustomSetPasswordForm(SetPasswordForm):
    def clean_new_password2(self):
        print(self.cleaned_data.keys())
        passwd1 = self.cleaned_data['new_password1']
        passwd2 = self.cleaned_data['new_password2']

        if passwd1 and passwd2:
            # Check that passwords match
            if passwd1 != passwd2:
                self.add_error('new_password2', 'The passwords do not match.')

            # Check password requirements
            if len(passwd1) < 8:
                self.add_error('new_password1', "Password must be 8-100 characters")
            if not schema1.validate(passwd1):
                self.add_error('new_password1', "Password must have an uppercase and a lowercase letter")
            if not schema2.validate(passwd1):
                self.add_error('new_password1', "Password must contain a digit and no spaces")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-25 fs-400 ff-sans-normal'
        self.helper.field_class='col-75'
        self.helper.form_tag = False