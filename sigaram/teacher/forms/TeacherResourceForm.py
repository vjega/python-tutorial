from django.utils.translation import (ugettext as _,)
from django import forms
from crispy_forms.helper import FormHelper
from portaladmin import models
#from crispy_forms.layout import Submit
class TeacherResourceForm(forms.Form):
    resourcetype  = forms.ChoiceField(
        label      = _("Category"),
        required   = True,
        choices    = [('text', 'Text'), ('audio', 'Audio'),('video','Video'), ('image', 'Image')]
    )
    fileurl = forms.CharField(
        label = _("Choose File"),
        max_length = 100,
        required = True,
        widget = forms.HiddenInput({ "placeholder": _("Email Id")})
    )
    schoolid = forms.ChoiceField(
        label    = _("Select School"),
        required = True,
        choices  = [(opt.schoolid, opt.schoolname) for opt in models.Schoolinfo.objects.all()],
    )
    originaltext = forms.CharField(
        label    = _("Title"),
        required = True,
        widget   = forms.Textarea({ "class": "summernote"})
    )
    resourcetitle = forms.CharField(
        label    = _("Note"),
        required = True,
        widget   = forms.Textarea({ "class": "summernote"})
    )
    def __init__(self, *args, **kwargs):
        super(TeacherResourceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'add-teacherresource'
        self.helper.form_class  = 'form-horizontal'
        self.helper.label_class = 'col-sm-4'
        self.helper.field_class = 'col-sm-8'
