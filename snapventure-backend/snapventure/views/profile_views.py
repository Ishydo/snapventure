from django.views.generic import DetailView, ListView, UpdateView, CreateView, TemplateView, DeleteView
from ..models import Journey, Scan, Step
from ..forms import UserForm, ProfileForm

from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin

class Statistics(LoginRequiredMixin, TemplateView):
    '''A view for the statistics on dashboard'''
    def get(self, request):
        context = {}
        context["nJourneys"] = Journey.objects.filter(creator=request.user.profile, deleted=False).count()
        context["nSteps"] = Step.objects.filter(journey__in=Journey.objects.filter(creator=request.user.profile, deleted=False)).count()
        context["nScans"] = Scan.objects.filter(
        step__in=Step.objects.filter(
            journey__in=Journey.objects.filter(creator=request.user.profile))
        ).count()
        context["nYScans"] = Scan.objects.filter(profile= request.user.profile).count()
        context["scanLogs"] = Scan.objects.filter(step__journey__in=Journey.objects.filter(creator=request.user.profile))
        return render(request, "snapventure/dashboard_statistics.html", context)

class Dashboard(LoginRequiredMixin, TemplateView):
    '''The dashboard view'''

    def get(self, request):
        context = {}
        context["current_user"] = request.user
        context["journeys"] = Journey.objects.filter(creator=request.user.profile, deleted=False)[:3]

        # Basic simple stats
        context["nJourneys"] = Journey.objects.filter(creator=request.user.profile, deleted=False).count()
        context["nSteps"] = Step.objects.filter(journey__in=Journey.objects.filter(creator=request.user.profile, deleted=False)).count()
        context["nScans"] = Scan.objects.filter(
        step__in=Step.objects.filter(
            journey__in=Journey.objects.filter(creator=request.user.profile))
        ).count()
        context["nYScans"] = Scan.objects.filter(profile= request.user.profile).count()

        return render(request, "snapventure/dashboard.html", context)

class Logout(TemplateView):
    '''The logout view'''

    def get(self, request):
        logout(request)
        return render(request, "snapventure/homepage.html")

class Register(TemplateView):
    '''The register view'''
    def get(self, request):
        return render(request, 'registration/register.html', {'user_form': UserCreationForm(),})
