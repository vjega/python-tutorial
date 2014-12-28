from django.utils.translation import (ugettext as _,)
from django import forms
from crispy_forms.helper import FormHelper
#from crispy_forms.layout import Submit
class StickyCommentForm(forms.Form):
    stickycomment  = forms.CharField(
        label     = _("Comment"),
        required  = True,
        widget    = forms.Textarea()
    )

    def __init__(self, *args, **kwargs):
        super(StickyCommentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'add-stickycomment'
        self.helper.form_class  = 'form-horizontal'
        self.helper.label_class = 'col-sm-4'
        self.helper.field_class = 'col-sm-8'
