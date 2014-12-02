from django.utils.translation import (ugettext as _,)
from django import forms
from crispy_forms.helper import FormHelper
#from crispy_forms.layout import Submit
class StudentresourceListForm(forms.Form):
    category       = forms.CharField(
        label      = _("Category"),
        max_length = 100,
        required   = True,
        widget     = forms.TextInput({ "placeholder": _("Category")})
    )
    choose_file    = forms.FileField(
        label      = _("Choose File"),
        max_length = 100,
        required   = True,
    )
    classname    = forms.ChoiceField(
        label    = _("Select Class"),
        required = True,
    )
    section      = forms.ChoiceField(
        label    = _("Select Section"),
        required = True,
    )
    studentsection = forms.ChoiceField(
        label      = _("Section"),
        required   = True,
    )
    Area         = forms.ChoiceField(
        label    = _("Select Area"),
        required = True,
    )
    short_photo    = forms.FileField(
        label      = _("Short Photo"),
        max_length = 100,
        required   = True,
    )
    heading      = forms.CharField(
        label    = _("Heading"),
        required = True,
        widget   = forms.Textarea({ "class": "summernote"})
    )
    def __init__(self, *args, **kwargs):
        super(StudentresourceListForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class  = 'form-horizontal'
        self.helper.label_class = 'col-sm-4'
        self.helper.field_class = 'col-sm-8'
