from django import forms
from .models import Profile, Journey, Inscription, Type, Step, Scan
from django.contrib.auth.models import User
from django.forms import modelformset_factory
from tinymce.widgets import TinyMCE

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'user']


class JourneyForm(forms.ModelForm):
    class Meta:
        model = Journey
        fields = ['name', 'description', 'img_description', 'img_ambiance', 'start_time', 'end_time', 'private', 'active']
        widgets = {'description': TinyMCE(attrs={'cols': 80, 'rows': 30})}


class StepForm(forms.ModelForm):
    class Meta:
        model = Step
        fields = ['name', 'content_text', 'position']


StepFormSet = modelformset_factory(Step, fields=['name', 'content_text', 'position'])
