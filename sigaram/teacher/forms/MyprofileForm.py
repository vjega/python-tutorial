from django.utils.translation import (ugettext as _,)
from django import forms
from crispy_forms.helper import FormHelper
from teacher import models
#from crispy_forms.layout import Submit

class MyprofileForm(forms.Form):   
    firstname = forms.CharField(
        label = _("Name"),
        max_length = 100,
        required = True,
        widget = forms.TextInput({ "placeholder": _("Name")})
    )
    password = forms.CharField(
        label = _("Password"),
        max_length = 100,
        required = True,
        widget = forms.TextInput({ "placeholder": _("Password")})
    )
    def __init__(self, *args, **kwargs):
        super(MyprofileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'update-profile-teacher'
        self.helper.form_class  = 'form-horizontal'
        self.helper.label_class = 'col-sm-4'
        self.helper.field_class = 'col-sm-8'
