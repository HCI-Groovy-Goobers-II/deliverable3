from django import forms
from crispy_forms.helper import FormHelper
from public_pages.models import HotJar

class HotJarForm(forms.ModelForm):
    hotjar_script = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': '4',
            'cols': '40',
            'placeholder': ('Paste your HotJar script here and'
                            ' it will be automatically injected on each page.')
        })
    )

    class Meta:
        model = HotJar
        fields = [ 'hotjar_script' ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-25 fs-400 ff-sans-normal'
        self.helper.field_class='col-75'
        self.helper.form_tag = False
