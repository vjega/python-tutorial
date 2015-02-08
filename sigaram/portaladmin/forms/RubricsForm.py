from django.utils.translation import (ugettext as _,)
from django import forms
from crispy_forms.helper import FormHelper
from teacher import models
#from crispy_forms.layout import Submit
class RubricsForm(forms.Form):
    Title = forms.CharField(
        label = _("Title"),
        max_length = 100,
        required = True,
        widget = forms.TextInput({ "placeholder": _("Title")})
    )
    Detail = forms.CharField(
        label = _("Detail"),
        required = True,
        widget = forms.TextInput({ "placeholder": _("Detail")})
    )
    instructions = forms.CharField(
        label = _("Instructions"),
        required = True,
        widget = forms.Textarea({ "class": "summernote"})
    )
    
    def __init__(self, *args, **kwargs):
        super(RubricsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'add-rubrics'
        self.helper.form_class  = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-10'
