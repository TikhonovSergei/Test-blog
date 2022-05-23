from django import forms
from django.conf import settings
from django.contrib.admin import widgets
from django.contrib.auth import authenticate
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField
from django.forms import Textarea, DateInput, ValidationError, RegexField
from datetime import date, time, datetime
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import *

class UserLogIn(AuthenticationForm):
    class Meta:
        model = User 
        fields = ['username', 'password']
             
    def clean(self):
        cleaned_data = super().clean()
        user_n = self.cleaned_data.get('username')
        password_n = self.cleaned_data.get('password')