from django.utils.translation import (ugettext as _,)
from django import forms
from crispy_forms.helper import FormHelper
#from crispy_forms.layout import Submit
class SchoolListForm(forms.Form):
    schoolname = forms.CharField(
        label = _("School Name"),
        max_length = 100,
        required = True,
        widget = forms.TextInput({ "placeholder": _("School Name")})
    )
    shortname = forms.CharField(
        label = _("Short Name"),
        max_length = 100,
        required = True,
        widget = forms.TextInput({ "placeholder": _("Short Name")})
    )
    description = forms.CharField(
        label = _("Reference"),
        max_length = 100,
        required = True,
        widget = forms.TextInput({ "placeholder": _("Reference")})
    )
    def __init__(self, *args, **kwargs):
        super(SchoolListForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'add-school'
        self.helper.form_class  = 'form-horizontal'
        self.helper.label_class = 'col-sm-4'
        self.helper.field_class = 'col-sm-8'
