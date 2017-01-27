from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, HttpResponse
from ..models import Step, Journey, Type, Scan, State, Inscription
from django.contrib import messages
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.utils import timezone

class ScanProcessView(TemplateView):
    '''
    The logic and tests to process when a scan is done by an user.
    The conditions to be able to see the content of a step are these :
     * You must be subscribed to the journey
     * If step is not root, you must have scanned the previous step
     * The journey must be active and in time
    '''
    def get(self, request, *args, **kwargs):
        context = {}
        step = Step.objects.get(qrcode_uuid=kwargs["qrcode_uuid"]) # The initial value for journey

        if not step.final:
            context["next_step"] = Step.objects.get(journey=step.journey, order_id=step.order_id  + 1)

        if step.journey.creator == request.user.profile:
            Scan(profile=request.user.profile, step=step, state=State.objects.get(code=800)).save()                          # Request user is creator ?
            return HttpResponseRedirect(reverse('step_detail', args=[step.slug]))
        else:
            if not self.journey_is_valid(step.journey):                              # Journey is valid ?
                return render(request, "snapventure/scan_error.html", {'message': 'This journey is no more online.'})
            else:
                if not self.journey_in_time(step.journey):                           # In time to play ?
                    return render(request, "snapventure/scan_error.html", {'message': 'This journey is out of time.'})
                else:
                    if not self.user_subscribed_to_journey(step.journey, request):   # Subscribed to journey ?
                        return render(request, "snapventure/scan_error.html", {'message': 'You are not subscribed to the journey.', 'journey': step.journey})
                    else:
                        if self.step_is_root(step):                                  # First step ?
                            Scan(profile=request.user.profile, step=step, state=State.objects.get(code=800)).save()
                            return HttpResponseRedirect(reverse('step_detail', args=[step.slug]))
                        else:
                            if not self.user_scanned_previous_step(step, request):   # Scanned previous ?
                                return render(request, "snapventure/scan_error.html",
                                {'message': 'You did not scan the previous step.',
                                'journey': step.journey,
                                'previous_step': Step.objects.get(journey=step.journey, order_id=step.order_id - 1)})
                            else:
                                Scan(profile=request.user.profile, step=step, state=State.objects.get(code=800)).save()
                                return HttpResponseRedirect(reverse('step_detail', args=[step.slug]))


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
