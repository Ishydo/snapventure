from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django import forms
from .models import Profile, Journey, Inscription, Type, Step, Scan, Edge, State

class ProfileAdminForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = '__all__'


class ProfileAdmin(admin.StackedInline):
    model = Profile
    can_delete=False
    #form = ProfileAdminForm
    #list_display = ['bio', 'location']
    #readonly_fields = ['bio', 'location']



# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (ProfileAdmin, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


#admin.site.register(Profile, ProfileAdmin)


class JourneyAdminForm(forms.ModelForm):

    class Meta:
        model = Journey
        fields = '__all__'


class JourneyAdmin(admin.ModelAdmin):
    form = JourneyAdminForm
    list_display = ['name', 'created', 'last_updated', 'description', 'img_description', 'img_ambiance', 'start_time', 'end_time', 'private', 'active', 'deleted']
    #readonly_fields = ['name', 'created', 'last_updated', 'description', 'img_description', 'img_ambiance', 'start_time', 'end_time', 'private', 'active', 'deleted']

admin.site.register(Journey, JourneyAdmin)


class InscriptionAdminForm(forms.ModelForm):

    class Meta:
        model = Inscription
        fields = '__all__'


class InscriptionAdmin(admin.ModelAdmin):
    form = InscriptionAdminForm
    list_display = ['created', 'last_updated']
    #readonly_fields = ['name', 'created', 'last_updated']


admin.site.register(Inscription, InscriptionAdmin)

class EdgeAdminForm(forms.ModelForm):

    class Meta:
        model = Edge
        fields = '__all__'


class EdgeAdmin(admin.ModelAdmin):
    form = EdgeAdminForm
    list_display = ['parent', 'child', 'last_updated']
    #readonly_fields = ['name', 'created', 'last_updated']

admin.site.register(Edge, EdgeAdmin)


class StateAdminForm(forms.ModelForm):

    class Meta:
        model = State
        fields = '__all__'


class StateAdmin(admin.ModelAdmin):
    form = StateAdminForm
    list_display = ['code', 'name', 'description', 'last_updated']
    #readonly_fields = ['name', 'created', 'last_updated']

admin.site.register(State, StateAdmin)



class TypeAdminForm(forms.ModelForm):

    class Meta:
        model = Type
        fields = '__all__'


class TypeAdmin(admin.ModelAdmin):
    form = TypeAdminForm
    list_display = ['name', 'created', 'last_updated', 'description']
    #readonly_fields = ['name', 'created', 'last_updated', 'description']

admin.site.register(Type, TypeAdmin)


class StepAdminForm(forms.ModelForm):

    class Meta:
        model = Step
        fields = '__all__'


class StepAdmin(admin.ModelAdmin):
    form = StepAdminForm
    list_display = ['name', 'created', 'last_updated', 'content_text', 'content_url', 'qrcode_uuid', 'final']
    #readonly_fields = ['name', 'created', 'last_updated', 'content_text', 'content_url', 'order_id', 'qrcode_uuid', 'final']

admin.site.register(Step, StepAdmin)

class ScanAdminForm(forms.ModelForm):

    class Meta:
        model = Scan
        fields = '__all__'


class ScanAdmin(admin.ModelAdmin):
    form = ScanAdminForm
    list_display = ['profile', 'step', 'state', 'created', 'last_updated']
    #readonly_fields = ['name', 'created', 'last_updated']

admin.site.register(Scan, ScanAdmin)
