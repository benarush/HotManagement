from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username' , 'email' , 'password1' , 'password2']


# the form.ModelForm is the module that handle forms...
class UserUpdateForm(forms.ModelForm):
#   here we are adding an email field and set it to EmailField type (its automatic handle invalid emails...)
    email = forms.EmailField()
#   The meta data class is handle overrites of parameters of behavior of the form
    class Meta:
#   The model Varriable is for tell the form witch model/db-table gonna be affected after save
        model = User
#   the fields varriable is handle witch order and witch fields to display for the form
        fields = ['username' , 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["image" , "gender"]
