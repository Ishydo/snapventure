from django.views.generic import DetailView, ListView, UpdateView, CreateView, TemplateView, DeleteView, View
from ..models import Journey, Profile, Inscription
from ..forms import JourneyForm
from django.core.urlresolvers import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from django.utils import timezone

# Creation de journey
class JourneyCreateView(CreateView):
    model = Journey
    form_class = JourneyForm

    # def post avec le renvoi des erreurs ?
    # http://kevindias.com/writing/django-class-based-views-multiple-inline-formsets/

    def form_valid(self, journey_form):
        self.object = journey_form.save(commit=False) # Used by the success_url
        new_journey = journey_form.save(commit=False) # Uncommitted to add creator
        new_journey.creator = self.request.user.profile # Add creator (request user)
        new_journey.save() # Final save
        return HttpResponseRedirect(self.get_success_url()) # Success url redirect

    # Redirection sur la pge de creation des steps
    def get_success_url(self):
        return reverse_lazy('add_journey_step', kwargs={'slug': self.object.slug})


class JourneyDetailView(DetailView):
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
    def get(self, request, *args, **kwargs):
        j = Journey.objects.get(pk=self.kwargs["pk"])

        if Inscription.objects.filter(profile=request.user.profile, journey=j).exists():
            Inscription.objects.filter(profile=request.user.profile, journey=j).delete()
        else:
            Inscription(profile=request.user.profile, journey=j).save()
        return redirect('journey_detail', slug=j.slug)


class JourneyListView(ListView):
    model = Journey

    def get_context_data(self, **kwargs):
        context = super(JourneyListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class JourneyUpdateView(UpdateView):
    model = Journey
    form_class = JourneyForm

class JourneyDeleteView(DeleteView):
    model = Journey
    success_url = reverse_lazy('dashboard')
