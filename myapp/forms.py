from django import forms
from .models import *

class signupform(forms.ModelForm):
    class Meta:
        model=usersignup
        fields='__all__'

class updateForm(forms.ModelForm):
    class Meta:
        model=usersignup
        fields=['firstname','lasttname','username','password','city','state','mobile']

class notesform(forms.ModelForm):
    class Meta:
        model=mynotes
        fields='__all__'

class contactForm(forms.ModelForm):
    class Meta:
        model=contactus
        fields='__all__'
        