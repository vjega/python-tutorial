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
    """resource_file = forms.FileField(
        label      = _("Choose File"),
        max_length = 100,
        required   = True,
    )"""
    schoolid = forms.ChoiceField(
        label    = _("Select School"),
        required = True,
        choices  = [(opt.schoolid, opt.schoolname) for opt in models.Schoolinfo.objects.all()],
    )
    classid = forms.ChoiceField(
        label    = _("Select Class"),
        required = True,
        choices  = [(opt.classid, opt.shortname) for opt in models.Classinfo.objects.all()],
    )
    section      = forms.ChoiceField(
        label    = _("Select Section"),
        required = True,
        choices  = [('a', 'A'), ('b','B')]
    )
    resourcecategory = forms.ChoiceField(
        label        = _("Select Division"),
        required     = True,
        choices      = [('0', 'Listening Comprehension'), ('1', 'Sample Lesson Plan')]
    )
    chapterid    = forms.ChoiceField(
        label    = _("Chapter"),
        required = True,
    )
    resourcetitle = forms.CharField(
        label    = _("Heading"),
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
