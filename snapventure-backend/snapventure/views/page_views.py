from django.views.generic import DetailView, ListView, UpdateView, CreateView, TemplateView, DeleteView

from django.shortcuts import render

class Home(TemplateView):
    '''Homepage simple view'''
    def get(self, request):
        return render(request, "snapventure/homepage.html")
