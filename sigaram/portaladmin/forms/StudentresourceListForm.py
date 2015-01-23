from django.utils.translation import (ugettext as _,)
from django import forms
from crispy_forms.helper import FormHelper
from portaladmin import models
#from crispy_forms.layout import Submit
class StudentresourceListForm(forms.Form):
    categoryid     = forms.ChoiceField(
        label      = _("Type"),
        required   = True,
        choices    = [('text', 'Text'),('image', 'Image'),('video', 'Video')
                         ]
    )
    fileurl = forms.CharField(
        label = _("Photo"),
        max_length = 100,
        required = True,
        widget = forms.HiddenInput({ "placeholder": _("Email Id")})
    )
    thumbnailurl = forms.CharField(
        label = _("Photo"),
        max_length = 100,
        required = True,
        widget = forms.HiddenInput({ "placeholder": _("Email Id")})
    )
    classid      = forms.ChoiceField(
        label    = _("Select Class"),
        required = True,
        choices  = [(opt.classid, opt.shortname) for opt in models.Classinfo.objects.all()],
    )
    section      = forms.ChoiceField(
        label    = _("Class"),
        required = True,
        choices  = [('a', 'A'), ('b','B')]
    )
    resourcetype = forms.ChoiceField(
        label    = _("Component"),
        required = True,
        choices  = [('0', 'Reading'), ('1','Picture conversation'),('2','Doodle Board'),('3','Picture composition')]
    )
    chapterid    = forms.ChoiceField(
        label    = _("Lessons "),
        required = True,
    )
    resourcetitle = forms.CharField(
        label     = _("Title"),
        required  = True,
        widget    = forms.Textarea({ "class": "summernote"})
    )
    resourcedescription  = forms.CharField(
        label     = _("Note"),
        required  = True,
        widget    = forms.Textarea({ "class": "summernote"})
    )
    def __init__(self, *args, **kwargs):
        super(StudentresourceListForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'add-studentresource'
        self.helper.form_class  = 'form-horizontal'
        self.helper.label_class = 'col-sm-4'
        self.helper.field_class = 'col-sm-8'
