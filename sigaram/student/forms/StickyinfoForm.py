from django.utils.translation import (ugettext as _,)
from django import forms
from crispy_forms.helper import FormHelper
#from teacher import models
#from crispy_forms.layout import Submit
class StickyinfoForm(forms.Form):
    title = forms.CharField(
        label = _("Title"),
        max_length = 250,
        required = True,
        widget = forms.TextInput({ "placeholder": _("Title")})
    )
    def __init__(self, *args, **kwargs):
        super(StickyinfoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'add-sticky-info'
        self.helper.form_class  = 'form-horizontal'
        self.helper.label_class = 'col-sm-1'
        self.helper.field_class = 'col-sm-11'
