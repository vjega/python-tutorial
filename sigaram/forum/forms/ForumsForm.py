from django.utils.translation import (ugettext as _,)
from django import forms
from crispy_forms.helper import FormHelper

#from crispy_forms.layout import Submit
class ForumsForm(forms.Form):
    forumname = forms.CharField(
        label = _("Title"),
        max_length = 100,
        required = True,
        widget = forms.TextInput({ "placeholder": _("Title")})
    )
    
    def __init__(self, *args, **kwargs):
        super(ForumsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'add-forum'
        self.helper.form_class  = 'form-horizontal'
        self.helper.label_class = 'col-sm-1'
        self.helper.field_class = 'col-sm-11'
