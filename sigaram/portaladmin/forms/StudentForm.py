from django.utils.translation import (ugettext as _,)
from django import forms
from crispy_forms.helper import FormHelper
from portaladmin import models
#from crispy_forms.layout import Submit

class StudentForm(forms.Form):
    schoolid = forms.ChoiceField(
        label = _("Select School"),
        required = True,
        choices  = [(opt.schoolid, opt.schoolname) for opt in models.Schoolinfo.objects.all().order_by('schoolname')],
    )
    classid = forms.ChoiceField(
        label = _("Class"),
        required = True,
        choices  = [(opt.classid, opt.shortname) for opt in models.Classinfo.objects.all()],
    )
    firstname = forms.CharField(
        label = _("Name"),
        max_length = 100,
        required = True,
        widget = forms.TextInput({ "placeholder": "%s %s"%(_("First"),_("Name"))})
    )
    # lastname = forms.CharField(
    #     label = "%s %s"%(_("last"),_("Name")),
    #     max_length = 100,
    #     required = True,
    #     widget = forms.TextInput({ "placeholder": "%s %s"%(_("Last"),_("Name"))})
    # )
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
    emailid = forms.CharField(
        label = _("Email Id"),
        max_length = 100,
        required = True,
        widget = forms.TextInput({ "placeholder": _("Email Id")})
    )
    imageurl = forms.CharField(
        label = _("Photo"),
        max_length = 100,
        required = True,
        widget = forms.HiddenInput({ "placeholder": _("Email Id")})
    )
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'add-student'
        self.helper.form_class  = 'form-horizontal'
        self.helper.label_class = 'col-sm-4'
        self.helper.field_class = 'col-sm-8'
