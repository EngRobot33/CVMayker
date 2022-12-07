from django import forms

from .models import *


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('title', 'link',)


class JobSeekerForm(forms.ModelForm):
    class Meta:
        model = JobSeeker
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'skills',)


class SkillCreateForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ('title', )
