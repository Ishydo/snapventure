from django.views.generic import DetailView, ListView, UpdateView, CreateView, TemplateView, DeleteView
from ..models import Journey
from ..forms import UserForm, ProfileForm

from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render



class Dashboard(TemplateView):
    template_name = "snapventure/dashboard.html"

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, "registration/login.html")
        else:
            context = {}
            context["current_user"] = request.user
            context["journeys"] = Journey.objects.filter(creator=request.user.profile, deleted=False)
            return render(request, self.template_name, context)

class Logout(TemplateView):
    template_name = "snapventure/homepage.html"

    def get(self, request):
        logout(request)
        return render(request, self.template_name)

class Register(TemplateView):

    def get(self, request):
        '''
        user_form = UserForm()
        profile_form = ProfileForm()
        return render(request, 'registration/register.html', {
                'user_form': user_form,
                'profile_form': profile_form
            })
'''
        return render(request, 'registration/register.html', {
                'user_form': UserCreationForm(),
            })
