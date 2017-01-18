from django.views.generic import DetailView, ListView, UpdateView, CreateView, TemplateView, DeleteView

from django.shortcuts import render

class Home(TemplateView):
    template_name = "snapventure/homepage.html"

    def get(self, request):
        return render(request, self.template_name)
