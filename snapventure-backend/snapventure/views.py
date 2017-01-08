from django.views.generic import DetailView, ListView, UpdateView, CreateView, TemplateView, DeleteView
from .models import Profile, Journey, Inscription, Type, Step, Scan, Edge, State

from django.contrib.auth import logout
from django.contrib.auth.models import User

from django.core.urlresolvers import reverse_lazy

from .forms import ProfileForm, JourneyForm, InscriptionForm, TypeForm, StepForm, ScanForm, StepFormSet

from django.forms import modelformset_factory
from django.db import IntegrityError, transaction

# For standard views
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.shortcuts import render

from django.utils import timezone
from django.utils.text import slugify

import qrcode
import base64
import os


class Home(TemplateView):
    template_name = "snapventure/homepage.html"

    def get(self, request):
        return render(request, self.template_name)


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

    def get_context_data(self, **kwargs):
        context = super(JourneyDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

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

    def create_qrcode(self, uuid):

        if not os.path.exists("qrcodes/" + uuid + ".jpg"):
            print("QRCODE CREATED")
            qr = qrcode.QRCode(version=5, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=30)
            qr.add_data("http://localhost:8000/scan/" + uuid)
            qr.make()

            img = qr.make_image()
            img.save("qrcodes/" + uuid + ".jpg", "JPEG")

    def get_initial(self):
        j = Journey.objects.get(slug=self.kwargs['slug'])
        return {'journey': j}

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

        new_step.save() # Final save

        if self.add_another:
            return HttpResponseRedirect("") # Success url redirect
        else:
            return HttpResponseRedirect("/dashboard/") # Success url redirect


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


class Logout(TemplateView):
    template_name = "snapventure/homepage.html"

    def get(self, request):
        logout(request)
        return render(request, self.template_name)

# App related views
class Index(TemplateView):
    template_name = "index.html"
    def get(self, request):

        # https://docs.djangoproject.com/en/dev/ref/models/querysets/#first
        # exists

        testU = User.objects.get(username="TestUser1")
        testStep = Step.objects.get(name__contains="Step 3")

        j = Journey.objects.first()
        usrs = User.objects.all()
        steps = Step.objects.filter(journey=j)
        inscriptions = j.inscriptions.all()

        test_scan(testStep, testU.profile)

        return render(request, self.template_name, {'journey' : j, 'users' : usrs, 'inscriptions' : inscriptions, 'steps': steps})


class Scanner(TemplateView):
    template_name = "scan.html"

    def get(self, request, uid):

        # Test prototype of test_scan function
        def test_scan(step, user):

            # Check authentication first :)

            # Check if user started the journey
            if Inscription.objects.filter(journey=step.journey, profile=user).exists():
                if step.root:
                    print("User scanned root step for this journey")
                    Scan(step=step, profile=user, state=State.objects.get(code=800)).save()
                    print("User scanned first code ;)")
                else:
                    # Get parent step of scanned step
                    directParent = Step.objects.get(parent_node__child=step)

                    # Do we have a valid scan for the parent ?
                    if directParent.scan_set.filter(state__code=800, profile=user).exists():
                        print("User scanned parent. Ok.")

                        # User already scanned this code ?
                        if step.scan_set.filter(state__code=800, profile=user).exists():
                            print("User already scanned this step.")
                        else:
                            Scan(step=step, profile=user, state=State.objects.get(code=800)).save()
                            print("Everything ok, add code 800 scan and show related content.")
                    else:
                        print("Previous node note scanned by user. Error.")
                        # Here get last scanned parent and tell user to go
            else:
                print("User must start the journey !")
                Inscription(journey = step.journey, profile=user).save()
                print("User subscribed to journey.")


        # The chosen user for the example
        pro = User.objects.get(username__contains="TestUser6").profile

        # Does the step with that uid exists ?
        if Step.objects.filter(qrcode_uuid=uid).exists():
            print("Looks like the uid is valid")

            # Currently scanned step
            scannedStep = Step.objects.get(qrcode_uuid=uid)

            # Test qrcode generation
            qr = qrcode.QRCode(version=5, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=30)
            qr.add_data("http://localhost:8000/snapventure/scan/" + str(scannedStep.qrcode_uuid))
            qr.make()

            img = qr.make_image()
            img.save("qrcodes/" + str(scannedStep.qrcode_uuid) + ".jpg", "JPEG")

            # Steps from the same journey
            journeySteps = Step.objects.filter(journey=scannedStep.journey)

            # Trigger a scan
            test_scan(scannedStep, pro)

        else:
            print("Invalid step uid.")

        return render(request, self.template_name, {"uid": uid, "journeySteps": journeySteps})


# API related views
class ProfileListView(ListView):
    model = Profile


class ProfileCreateView(CreateView):
    model = Profile
    form_class = ProfileForm


class ProfileDetailView(DetailView):
    model = Profile


class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileForm



class InscriptionListView(ListView):
    model = Inscription


class InscriptionCreateView(CreateView):
    model = Inscription
    form_class = InscriptionForm


class InscriptionDetailView(DetailView):
    model = Inscription


class InscriptionUpdateView(UpdateView):
    model = Inscription
    form_class = InscriptionForm


class TypeListView(ListView):
    model = Type


class TypeCreateView(CreateView):
    model = Type
    form_class = TypeForm


class TypeDetailView(DetailView):
    model = Type


class TypeUpdateView(UpdateView):
    model = Type
    form_class = TypeForm



class ScanListView(ListView):
    model = Scan


class ScanCreateView(CreateView):
    model = Scan
    form_class = ScanForm


class ScanDetailView(DetailView):
    model = Scan


class ScanUpdateView(UpdateView):
    model = Scan
    form_class = ScanForm
