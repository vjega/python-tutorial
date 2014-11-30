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
    school = forms.ChoiceField(
        label = _("Select School"),
        required = True,
    )
    classname = forms.ChoiceField(
        label = _("Select Class"),
        required = True,
    )
    division = forms.ChoiceField(
        label = _("Select Division"),
        required = True,
    )
    part = forms.ChoiceField(
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
