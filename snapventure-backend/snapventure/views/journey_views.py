from django.views.generic import DetailView, ListView, UpdateView, CreateView, TemplateView, DeleteView, View
from ..models import Journey, Profile, Inscription
from ..forms import JourneyForm
from django.core.urlresolvers import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.shortcuts import render

class JourneyCreateView(CreateView):
    ```View for a journey creation```
    model = Journey
    form_class = JourneyForm

    def form_valid(self, journey_form):
        self.object = journey_form.save(commit=False) # Used by the success_url
        new_journey = journey_form.save(commit=False) # Uncommitted to add creator
        new_journey.creator = self.request.user.profile # Add creator (request user)
        new_journey.save() # Final save
        return HttpResponseRedirect(self.get_success_url()) # Success url redirect

    # Redirect on step creation page
    def get_success_url(self):
        return reverse_lazy('add_journey_step', kwargs={'slug': self.object.slug})

class JourneyDetailView(DetailView):
    ```View for a journey detail```
    model = Journey

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        if not request.user.is_authenticated:
            context["register"] = True
        else:
            if not Inscription.objects.filter(journey=self.object, profile=request.user.profile).exists():
                context["subscribe"] = True
            else:
                context["subscribe"] = False
        return self.render_to_response(context)


class JourneySubscribe(LoginRequiredMixin, View):
    ```View for a subscribtion toggle```
    def get(self, request, *args, **kwargs):
        j = Journey.objects.get(pk=self.kwargs["pk"])

        if Inscription.objects.filter(profile=request.user.profile, journey=j).exists():
            Inscription.objects.filter(profile=request.user.profile, journey=j).delete()
        else:
            Inscription(profile=request.user.profile, journey=j).save()
        return redirect('journey_detail', slug=j.slug)


class JourneyManagement(LoginRequiredMixin, TemplateView):
    ```View to manage a user's personal journeys```
    def get(self, request, *args, **kwargs):
        journeys = Journey.objects.filter(creator=request.user.profile)
        return render(request, "snapventure/journey_management.html", {'journeys': journeys})

class JourneyListView(ListView):
    ```The list view for a journey```
    model = Journey

    def get_context_data(self, **kwargs):
        context = super(JourneyListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class JourneyUpdateView(UpdateView):
    ```Journey update view```
    model = Journey
    form_class = JourneyForm

class JourneyDeleteView(DeleteView):
    ```Delete journey view```
    model = Journey
    success_url = reverse_lazy('dashboard')
