from django.utils.translation import (ugettext as _,)
from django import forms
from crispy_forms.helper import FormHelper
#from crispy_forms.layout import Submit
class CalendarForm(forms.Form):
    title = forms.CharField(
        label = _("Event Title"),
        max_length = 100,
        required = True,
        widget = forms.TextInput({ "placeholder": _("Event Title")})
    )
    start = forms.CharField(
        label = _("Start Time"),
        max_length = 100,
        required = True,
        widget = forms.TextInput({ "placeholder": _("Start Time")})
    )
    end = forms.CharField(
        label = _("End Time"),
        max_length = 100,
        required = True,
        widget = forms.TextInput({ "placeholder": _("End Time")})
    )
    alldayevents = forms.CharField(
        label = _("All Day Events"),
        widget = forms.CheckboxInput()
    )
    
    def __init__(self, *args, **kwargs):
        super(CalendarForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'cal-event'
        self.helper.form_class  = 'form-horizontal'
        self.helper.label_class = 'col-sm-4'
        self.helper.field_class = 'col-sm-8'
        self.helper.label_size = ' col-sm-offset-3'
