from django.utils.translation import (ugettext as _,)
from django import forms
from crispy_forms.helper import FormHelper
#from crispy_forms.layout import Submit
class TeacherResourceForm(forms.Form):
    resource_file = forms.FileField(
        label = _("Choose File"),
        max_length = 100,
        required = True,
    )
    school = forms.CharField(
        label = _("Select School"),
         max_length = 100,
        required = True,
        widget = forms.TextInput({ "placeholder": _("User Name")})
    )
    classname = forms.CharField(
        label = _("Select Class"),
         max_length = 100,
        required = True,
        widget = forms.TextInput({ "placeholder": _("Select Class")})
    )
    division = forms.CharField(
        label = _("Select Division"),
         max_length = 100,
        required = True,
        widget = forms.TextInput({ "placeholder": _("User Name")})
    )
    part = forms.CharField(
        label = _("Select Part"),
        required = True,
    )
    heading = forms.CharField(
        label = _("Heading"),
        required = True,
        widget = forms.Textarea({ "class": "summernote"})
    )
    def __init__(self, *args, **kwargs):
        super(TeacherResourceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class  = 'form-horizontal'
        self.helper.label_class = 'col-sm-4'
        self.helper.field_class = 'col-sm-8'
