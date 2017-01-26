from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, HttpResponse
from ..models import Step, Journey, Type, Scan, State

class ScanProcessView(TemplateView):

    def get(self, request, qrcode_uuid):

        # the step
        step = Step.objects.get(qrcode_uuid=qrcode_uuid) # The initial value for journey

        if not request.user.is_authenticated():
            return HttpResponse("not auth")
        else:
            if step.root:
                if self.user_already_scanned_step(step, request):
                    print("Already scanned")
                    return HttpResponse("ok root")
                else:
                    print("Step is root - Add Scan")
                    Scan(profile=request.user.profile, step=step, state=State.objects.get(code=800)).save()
                    print("Scan with code 800 added successfully")
                    return HttpResponse("ok scanned")
            else:
                if not self.user_scanned_previous_step(step, request):
                    return HttpResponse("notscanned previous")
                else:
                # add scan if last scaned
                    Scan(profile=request.user.profile, step=step, state=State.objects.get(code=800)).save()
                    return HttpResponse("ok pass to view")


    def user_scanned_previous_step(self, step, request):
        return Scan.objects.filter(profile=request.user.profile, step=Step.objects.get(journey=step.journey, order_id=step.order_id - 1)).exists()

    def user_already_scanned_step(self, step, request):
        return Scan.objects.filter(step=step, profile=request.user.profile, state=State.objects.get(code=800)).exists()
