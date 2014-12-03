from django.utils.translation import (ugettext as _,)
from django import forms
from crispy_forms.helper import FormHelper
#from crispy_forms.layout import Submit
class ClassListForm(forms.Form):
    classname = forms.ChoiceField(
        label = _("Class Name"),
        max_length = 100,
        required = True,
        widget = forms.TextInput({ "placeholder": _("Class Name")})
    )
    shortname = forms.ChoiceField(
        label = _("Short Name"),
        max_length = 100,
        required = True,
        widget = forms.TextInput({ "placeholder": _("Short Name")})
    )
    def __init__(self, *args, **kwargs):
        super(ClassListForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'add-classlist'
        self.helper.form_class  = 'form-horizontal'
        self.helper.label_class = 'col-sm-4'
        self.helper.field_class = 'col-sm-8'
