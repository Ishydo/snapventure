from django.views.generic import DetailView, ListView, UpdateView, CreateView, TemplateView, DeleteView
from ..models import Journey, Scan, Step
from ..forms import UserForm, ProfileForm

from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin

class Statistics(LoginRequiredMixin, TemplateView):
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

class Dashboard(TemplateView):
    template_name = "snapventure/dashboard.html"

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, "registration/login.html")
        else:
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

            return render(request, self.template_name, context)

class Logout(TemplateView):
    template_name = "snapventure/homepage.html"

    def get(self, request):
        logout(request)
        return render(request, self.template_name)

class Register(TemplateView):
    def get(self, request):
        return render(request, 'registration/register.html', {'user_form': UserCreationForm(),})
