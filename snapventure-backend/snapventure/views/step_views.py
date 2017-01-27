from django.views.generic import DetailView, ListView, UpdateView, CreateView, TemplateView, DeleteView
from ..models import Step, Journey, Type, Scan, Inscription
from ..forms import StepForm
from django.core.urlresolvers import reverse_lazy

from django.utils.text import slugify
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin

from django.utils import timezone

import qrcode
import base64
import os

# Creation flow step add steps
class StepFirstCreateView(CreateView):
    model = Step
    form_class = StepForm

    def get(self, request, *args, **kwargs):

        j = Journey.objects.get(slug=self.kwargs['slug']) # The initial value for journey
        t = Type.objects.get(name="Rich Text") # Initial value for content type in first version

        self.object = None
        step_form = StepFormSet(queryset=Step.objects.filter(journey=j), initial=[{'journey':j, 'content_type': t}])
        return self.render_to_response(self.get_context_data(step_form=step_form))

    def post(self, request, *args, **kwargs):
        self.object = None
        step_form = StepFormSet(self.request.POST)

        if(step_form.is_valid()):

            j = Journey.objects.get(slug=self.kwargs['slug']) # The journey associated
            new_steps = []

            for form in step_form:
                step = form.save(commit=False)
                step.journey = j
                step.content_type = Type.objects.get(name="Rich Text") # Default type for v1
                print("One uuid step is " + str(step.qrcode_uuid))
                self.create_qrcode(str(step.qrcode_uuid))
                new_steps.append(step)
                #step.save()
            try:
                with transaction.atomic():
                    Step.objects.filter(journey=j).delete()
                    Step.objects.bulk_create(new_steps)
                    return HttpResponse("Created ok ATOMIC")
            except IntegrityError:
                return HttpResponse("Integrity error")
        else:
            return HttpResponse("nope")



class StepCreateView(CreateView):
    model = Step
    form_class = StepForm
    add_another = False

    def get(self, request, *args, **kwargs):
        self.object = None
        j = Journey.objects.get(slug=self.kwargs['slug'])
        steps = Step.objects.filter(journey=j).order_by('order_id')
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(form=form, steps=steps))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if (form.is_valid()):
            if "save_and_add_another" in request.POST:
                self.add_another = True
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, step_form):

        j = Journey.objects.get(slug=self.kwargs['slug'])
        t = Type.objects.get(name="Rich Text")

        self.object = step_form.save(commit=False) # Used by the success_url
        new_step = step_form.save(commit=False)
        new_step.journey = j # The associated journey
        new_step.content_type = t # Default content type for snapventure v1
        new_step.slug = slugify(new_step.name) # Create slug

        # Order ID
        if Step.objects.filter(journey=j).count() == 0:
            print("It's the first step of this journey")
            new_step.root = True
            new_step.order_id = 1
        else:
            print("It's not the first step")
            new_step.order_id = Step.objects.filter(journey=j).count() + 1
        self.create_qrcode(str(new_step.qrcode_uuid)) # Create the qrcode image and save it
        new_step.save() # Final save

        if self.add_another:
            return HttpResponseRedirect("") # Success url redirect
        else:
            return HttpResponseRedirect("/dashboard/") # Success url redirect


    def create_qrcode(self, uuid):
        if not os.path.exists("qrcodes/" + uuid + ".jpg"):
            print("QRCODE CREATED")
            qr = qrcode.QRCode(version=5, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=30)
            qr.add_data("http://localhost:8000/scan/" + uuid)
            qr.make()

            img = qr.make_image()
            img.save("qrcodes/" + uuid + ".jpg", "JPEG")

class StepManageView(TemplateView):
    template_name = "snapventure/steps_manage.html"

    def get(self, request, *args, **kwargs):
        j = Journey.objects.get(slug=self.kwargs['slug'])
        steps = Step.objects.filter(journey=j).order_by("order_id")
        return render(request, self.template_name, {'journey': j, 'steps': steps})


class StepDetailView(LoginRequiredMixin, DetailView):
    model = Step

    def get(self, request, *args, **kwargs):

        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        if not self.object.final:
            context["next_step"] = Step.objects.get(journey=self.object.journey, order_id=self.object.order_id  + 1)

        if self.object.journey.creator == request.user.profile:                             # Request user is creator ?
            return self.render_to_response(context)
        else:
            if not self.journey_is_valid(self.object.journey):                              # Journey is valid ?
                return render(request, "snapventure/scan_error.html", {'message': 'This journey is no more online.'})
            else:
                if not self.journey_in_time(self.object.journey):                           # In time to play ?
                    return render(request, "snapventure/scan_error.html", {'message': 'This journey is out of time.'})
                else:
                    if not self.user_subscribed_to_journey(self.object.journey, request):   # Subscribed to journey ?
                        return render(request, "snapventure/scan_error.html", {'message': 'You are not subscribed to the journey.', 'journey': self.object.journey})
                    else:
                        if self.step_is_root(self.object):                                  # First step ?
                            return self.render_to_response(context)
                        else:
                            if not self.user_scanned_previous_step(self.object, request):   # Scanned previous ?
                                return render(request, "snapventure/scan_error.html",
                                {'message': 'You did not scan the previous step.',
                                'journey': self.object.journey,
                                'previous_step': Step.objects.get(journey=self.object.journey, order_id=self.object.order_id - 1)})
                            else:
                                return self.render_to_response(context)


    def journey_is_valid(self, journey):
        return journey.active

    def journey_in_time(self, journey):
        if not journey.end_time:
            return True
        else:
            return journey.start_time <= timezone.now() <= journey.end_time

    def step_is_root(self, step):
        return step.root

    def user_scanned_previous_step(self, step, request):
        return Scan.objects.filter(profile=request.user.profile, step=Step.objects.get(journey=step.journey, order_id=step.order_id - 1)).exists()

    def user_subscribed_to_journey(self, journey, request):
        return Inscription.objects.filter(profile=request.user.profile, journey=journey).exists()


class StepUpdateView(UpdateView):
    model = Step
    form_class = StepForm


class StepDeleteView(DeleteView):
    model = Step
    success_url = reverse_lazy('dashboard')
