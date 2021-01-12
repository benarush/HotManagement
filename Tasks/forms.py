from django.forms import ModelForm
from .models import Task
from django import forms
from django import forms
from django.core import validators


class CreateTaskForm(forms.ModelForm):
    email_attached_file = forms.FileField()

    class Meta:
        model = Task
        fields = ['problem', 'weeks', 'description', 'email_attached_file', 'start_date']
