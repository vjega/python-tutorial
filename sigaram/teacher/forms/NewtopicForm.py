from django.utils.translation import (ugettext as _,)
from django import forms
from crispy_forms.helper import FormHelper

#from crispy_forms.layout import Submit
class NewtopicForm(forms.Form):
    topicname = forms.CharField(
        label    = _("Heading"),
        required = True,
        widget   = forms.Textarea({ "class": "summernote"})
    )
    def __init__(self, *args, **kwargs):
        super(NewtopicForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'newtopic-forum'
        self.helper.form_class  = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-10'
