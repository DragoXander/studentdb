from django import forms
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    name = forms.CharField(label='Your name', max_length=100)


class SemesterCreationForm(forms.Form):
    name = forms.CharField(label='Название семестра', max_length=100)
    number = forms.IntegerField(label='Номер семестра')
    course = forms.IntegerField(label='Номер курса')
