from django.utils.translation import (ugettext as _,)
from django import forms
from crispy_forms.helper import FormHelper
#from crispy_forms.layout import Submit
class StudentWorkSpaceForm(forms.Form):
    workspacetype  = forms.ChoiceField(
        label      = _("Category"),
        required   = True,
        choices    = [('text', 'Text'), ('audio', 'Audio'),('video','Video'), ('image', 'Image')]
    )
    workspacetitle = forms.CharField(
        label      = _("Title"),
        max_length = 100,
        required   = True,
        widget     = forms.Textarea({ "class": "summernote"})
    )
    workspacetext  = forms.CharField(
        label      = _("Note"),
        required   = True,
        widget     = forms.Textarea({ "class": "summernote"})
    )
    def __init__(self, *args, **kwargs):
        super(StudentWorkSpaceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'add-studentworkspace'
        self.helper.form_class  = 'form-horizontal'
        self.helper.label_class = 'col-sm-4'
        self.helper.field_class = 'col-sm-8'
