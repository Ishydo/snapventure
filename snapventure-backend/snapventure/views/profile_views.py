from django.views.generic import DetailView, ListView, UpdateView, CreateView, TemplateView, DeleteView
from ..models import Journey

from django.contrib.auth import logout
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
