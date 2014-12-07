from django.utils.translation import (ugettext as _,)
from django import forms
from crispy_forms.helper import FormHelper
#from crispy_forms.layout import Submit
class StudentWorkForm(forms.Form):
    workspacetype  = forms.ChoiceField(
        label      = _("Category"),
        required   = True,
        choices    = [('text', 'Text'), ('audio', 'Audio'),('video','Video'), 
                        ('image', 'Image')]
    )
    workspacetext  = forms.CharField(
        label    = _("Notes"),
        required = True,
        widget   = forms.Textarea({ "class": "summernote"})
    )
    workspacetitle = forms.CharField(
        label    = _("Title"),
        required = True,
        widget   = forms.Textarea({ "class": "summernote"})
    )
    
    def __init__(self, *args, **kwargs):
        super(StudentWorkForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'add-studentworkspace'
        self.helper.form_class  = 'form-horizontal'
        self.helper.label_class = 'col-sm-4'
        self.helper.field_class = 'col-sm-8'