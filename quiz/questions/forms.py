from django import forms
from .models import *
class RegistrationForm(forms.ModelForm):
    class Meta:
        model=Registration
        fields=['name','email','mobile']