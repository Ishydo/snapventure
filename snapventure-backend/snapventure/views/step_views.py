from django.views.generic import DetailView, ListView, UpdateView, CreateView, TemplateView, DeleteView
from ..models import Step, Journey, Type
from ..forms import StepForm
from django.core.urlresolvers import reverse_lazy

from django.utils.text import slugify
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.shortcuts import render


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


class StepDetailView(DetailView):
    model = Step

    def get_context_data(self, **kwargs):
        context = super(StepDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class StepUpdateView(UpdateView):
    model = Step
    form_class = StepForm


class StepDeleteView(DeleteView):
    model = Step
    success_url = reverse_lazy('dashboard')
