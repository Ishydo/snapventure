
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, HttpResponse
from ..models import Step, Journey, Type, Scan, State
from django.contrib import messages
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.utils import timezone

class ScanProcessView(TemplateView):

    def get(self, request, qrcode_uuid):

        # the step
        step = Step.objects.get(qrcode_uuid=qrcode_uuid) # The initial value for journey

        if not request.user.is_authenticated():
            messages.add_message(request, messages.INFO, 'You are not authenticated.')
            return render(request, "snapventure/scan_error.html", {'message': 'You are not authenticated.'})
        else:
            if not self.journey_is_valid(step.journey):
                return render(request, "snapventure/scan_error.html", {'message': 'This journey is no longer available.'})
            else:
                if not self.journey_in_time(step.journey):
                    return render(request, "snapventure/scan_error.html", {'message': 'This journey is out of time.'})
                else:
                    if step.root:
                        if self.user_already_scanned_step(step, request):
                            return HttpResponseRedirect(reverse('step_detail', args=[step.slug]))
                        else:
                            Scan(profile=request.user.profile, step=step, state=State.objects.get(code=800)).save()
                            return render(request, "snapventure/scan_error.html", {'message': 'You did not scan the previous step.'})
                    else:
                        if not self.user_scanned_previous_step(step, request):
                            return render(request, "snapventure/scan_error.html", {'message': 'You did not scan the previous step.'})
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

    def user_scanned_previous_step(self, step, request):
        return Scan.objects.filter(profile=request.user.profile, step=Step.objects.get(journey=step.journey, order_id=step.order_id - 1)).exists()

    def user_already_scanned_step(self, step, request):
        return Scan.objects.filter(step=step, profile=request.user.profile, state=State.objects.get(code=800)).exists()
