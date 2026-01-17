from django import forms 
from django.forms import CharField
from sentanapp.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name','address','email','gender','contact','place','district']

