from django.utils.translation import (ugettext as _,)
from django import forms
from crispy_forms.helper import FormHelper
#from crispy_forms.layout import Submit
class StudentListForm(forms.Form):
    school = forms.ChoiceField(
        label = _("Select School"),
        required = True,
    )
    classname = forms.ChoiceField(
        label = _("Select Class"),
        required = True,
    )
    name = forms.CharField(
        label = _("Name"),
        max_length = 100,
        required = True,
        widget = forms.TextInput({ "placeholder": _("Name")})
    )
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
        widget = forms.TextInput({ "placeholder": _("Password")})
    )
    emailid = forms.CharField(
        label = _("Email Id"),
        max_length = 100,
        required = True,
        widget = forms.TextInput({ "placeholder": _("Email Id")})
    )
    teacher_photo = forms.FileField(
        label = _("Choose File"),
        max_length = 100,
        required = True,
    )
    def __init__(self, *args, **kwargs):
        super(StudentListForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class  = 'form-horizontal'
        self.helper.label_class = 'col-sm-4'
        self.helper.field_class = 'col-sm-8'
