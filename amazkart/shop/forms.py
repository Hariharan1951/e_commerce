from django.contrib.auth.forms import UserCreationForm
from shop.models import User # Importing in-built `User` from models.py.
from django import forms

# Shop FORMS.PY file

class CustomUserForm(UserCreationForm): # To create our own custom form with required fields.
    
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"Enter User Name"})) # to overwrite the attributes (or) to add placeholders.
    email = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"Enter Email Address"})) 
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control", "placeholder":"Enter Your Password"})) 
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control", "placeholder":" Enter Confirm Password"})) 
    
    
    class Meta:
        model = User # In-built `User` is set to `model` variable to get our custom required fields. 
        fields = ["username", "email", "password1", "password2"]
        