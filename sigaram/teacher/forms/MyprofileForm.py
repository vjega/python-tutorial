from django.utils.translation import (ugettext as _,)
from django import forms
from crispy_forms.helper import FormHelper
from teacher import models
#from crispy_forms.layout import Submit

class MyprofileForm(forms.Form):   
    firstname = forms.CharField(
        label = _("First Name"),
        max_length = 100,
        required = True,
        widget = forms.TextInput({ "placeholder": _("Name")})
    )
    lastname = forms.CharField(
        label = _("Last Name"),
        max_length = 100,
        required = True,
        widget = forms.TextInput({ "placeholder": "%s %s"%(_("Last"),_("Name"))})
    )
    emailid = forms.CharField(
        label = _("Email Id"),
        max_length = 100,
        required = True,
        widget = forms.TextInput({ "placeholder": _("Email Id")})
    )
    password = forms.CharField(
        label = _("Password"),
        max_length = 100,
        required = True,
        widget = forms.TextInput({ "placeholder": _("Password")})
    )
    Photo = forms.CharField( 
        label = _("Photo"),
        max_length = 100,
        required = True,
        widget = forms.HiddenInput({ "placeholder": _("Email Id")})
    )

    def __init__(self, *args, **kwargs):
        super(MyprofileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'update-profile-teacher'
        self.helper.form_class  = 'form-horizontal'
        self.helper.label_class = 'col-sm-4'
        self.helper.field_class = 'col-sm-8'
