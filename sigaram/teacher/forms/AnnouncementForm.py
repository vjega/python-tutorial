from django.utils.translation import (ugettext as _,)
from django import forms
from crispy_forms.helper import FormHelper
from portaladmin import models
#from crispy_forms.layout import Submit
class AnnouncementForm(forms.Form):
    fileurl        = forms.CharField(
        label      = _("Photo"),
        max_length = 100,
        required   = True,
        widget     = forms.HiddenInput({ "placeholder": _("Email Id")})
    )
    messagetitle  = forms.CharField(
        label     = _("Title"),
        required  = True,
        widget    = forms.Textarea({ "class": "summernote"})
    )
    message       = forms.CharField(
        label     = _("Announcement"),
        required  = True,
        widget    = forms.Textarea({ "class": "summernote"})
    )
    def __init__(self, *args, **kwargs):
        super(AnnouncementForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'add-announcement'
        self.helper.form_class  = 'form-horizontal'
        self.helper.label_class = 'col-sm-4'
        self.helper.field_class = 'col-sm-8'
