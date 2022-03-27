from django import forms

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
    grade_level = forms.CharField(
        label='Choose grade level',
        required=True,
        widget=forms.Select(choices=SelectFieldChoices.GRADE_LEVEL_CHOICES)
    )