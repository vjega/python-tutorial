from django import forms

class SimpleForm(forms.Form):
    user_name = forms.CharField(label='Username', required=True)