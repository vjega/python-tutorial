from django.utils.translation import (ugettext as _,)
from django import forms
from crispy_forms.helper import FormHelper
#from crispy_forms.layout import Submit
class AdminForm(forms.Form):
    username = forms.CharField(
        label = _("User Name"),
        max_length = 100,
        required = True,
        widget = forms.TextInput({ "placeholder": _("User Name")})
    )
    password = forms.CharField(
        label = _("Password"),
        max_length = 100,
        required = True,
        widget = forms.PasswordInput({ "placeholder": _("Password")})
    )
    firstname = forms.CharField(
        label = "%s %s"%(_("First"),_("Name")),
        max_length = 100,
        required = True,
        widget = forms.TextInput({ "placeholder": "%s %s"%(_("First"),_("Name"))})
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
    image = forms.CharField(
        label = _("Photo"),
        max_length = 100,
        required = True,
        widget = forms.HiddenInput({ "placeholder": _("Email Id")})
    )
    def __init__(self, *args, **kwargs):
        super(AdminForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'add-admin'
        self.helper.form_class  = 'form-horizontal'
        self.helper.label_class = 'col-sm-4'
        self.helper.field_class = 'col-sm-8'
