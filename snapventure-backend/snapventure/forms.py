from django import forms
from .models import Profile, Journey, Inscription, Type, Step, Scan
from django.contrib.auth.models import User

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
        fields = ['name', 'description', 'img_description', 'img_ambiance', 'start_time', 'end_time', 'private', 'active', 'creator']
        widgets = {'creator': forms.HiddenInput()}

class InscriptionForm(forms.ModelForm):
    class Meta:
        model = Inscription
        fields = ['journey', 'profile']


class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ['name', 'description']


class StepForm(forms.ModelForm):
    class Meta:
        model = Step
        fields = ['name', 'content_text', 'content_url', 'final', 'content_type', 'journey']
        widgets = {'journey': forms.HiddenInput()}


class ScanForm(forms.ModelForm):
    class Meta:
        model = Scan
        fields = ['step', 'profile', 'state']
