from django import forms
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Column
from password_validator import PasswordValidator

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

    def clean_password(self):
        passwd = self.cleaned_data['password']
        if len(passwd) < 8:
            self.add_error('password', "Password must be 8-100 characters")
        if not schema1.validate(passwd):
            self.add_error('password', "Password must have an uppercase and a lowercase letter")
        if not schema2.validate(passwd):
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