from django.utils.translation import (ugettext as _,)
from django import forms
from crispy_forms.helper import FormHelper
from portaladmin import models

class TopicsForm(forms.Form):
    topicname  = forms.CharField(
        label     = _("Text of the note"),
        required  = True,
        widget    = forms.Textarea({ "class": "summernote"})
    )

    def __init__(self, *args, **kwargs):
        super(TopicsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'add-topic'
        self.helper.form_class  = 'form-horizontal'
        self.helper.label_class = 'col-sm-4'
        self.helper.field_class = 'col-sm-8'
