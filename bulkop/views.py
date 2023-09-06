from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.http import HttpResponse
from django.utils.translation import gettext_noop as _
from django.contrib import messages
from logs.views import addlogmsg

from computes.models import Compute
from instances.models import Instance
# Create your views here.

def bulkop(request):
    instances = None

    computes = (
        Compute.objects.all()
        .order_by("name")
        .prefetch_related("instance_set")
        .prefetch_related("instance_set__userinstance_set")
    )

    if request.user.is_superuser:
        instances = Instance.objects.all().prefetch_related("userinstance_set")
    else:
        instances = Instance.objects.filter(
            userinstance__user=request.user
        ).prefetch_related("userinstance_set")

    if not request.user.is_superuser:
        return HttpResponse("404")
        
    return render(
        request, "bulkoperations.html", {"computes": computes, "instances": instances}
    )

def bulkStart(request):
    if request.method == 'POST':
        data = request.POST
        for val in data:
            if val.startswith('instance-'):
                tempInstance = Instance.objects.get(pk=int(val[9:]))
                if (tempInstance.status != 1):
                    if tempInstance.is_template:
                        messages.warning(request, _("Templates cannot be started."))
                    else:
                        tempInstance.proxy.start()
                        addlogmsg(
                            request.user.username, tempInstance.compute.name, tempInstance.name, _("Power On")
                        )
    return redirect(request.META.get("HTTP_REFERER"))
    
def bulkForceOff(request):
    if request.method == 'POST':
        data = request.POST
        for val in data:
            if val.startswith('instance-'):
                tempInstance = Instance.objects.get(pk=int(val[9:]))
                if (tempInstance.status != 5):
                    if tempInstance.is_template:
                        messages.warning(request, _("Templates cannot be shutdown."))
                    else:
                        tempInstance.proxy.force_shutdown()
                        addlogmsg(
                            request.user.username, tempInstance.compute.name, tempInstance.name, _("Force Off")
                        )
    return redirect(request.META.get("HTTP_REFERER"))
    
def poweron(request, pk):
    instance = Instance.objects.get(pk=int(pk))
    if instance.is_template:
        messages.warning(request, _("Templates cannot be started."))
    else:
        instance.proxy.start()
        addlogmsg(
            request.user.username, instance.compute.name, instance.name, _("Power On")
        )
        return HttpResponse('') 

def forceoff(request, pk):
    instance = Instance.objects.get(pk=int(pk))
    if instance.is_template:
        messages.warning(request, _("Templates cannot be shutdown."))
    else:
        instance.proxy.force_shutdown()
        addlogmsg(
            request.user.username, instance.compute.name, instance.name, _("Force Off")
        )
        return HttpResponse('') 