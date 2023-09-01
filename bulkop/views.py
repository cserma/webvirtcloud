from django.shortcuts import render
from django.http import JsonResponse

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

    if request.user.is_superuser or request.user.has_perm("instances.view_instances"):
        instances = Instance.objects.all().prefetch_related("userinstance_set")
    else:
        instances = Instance.objects.filter(
            userinstance__user=request.user
        ).prefetch_related("userinstance_set")

    return render(
        request, "bulkoperations.html", {"computes": computes, "instances": instances}
    )



def bulkStart(request):
    if request.method == 'POST':
        selectedInstances = request.body.decode('utf-8').split(",")
        
        for selectedInstance in selectedInstances:
            tempInstance = Instance.objects.get(pk=int(selectedInstance))
            if (tempInstance.status != 1):
                tempInstance.proxy.start()
        
        return JsonResponse({'success': True})  
    

def bulkForceOff(request):
    if request.method == 'POST':
        selectedInstances = request.body.decode('utf-8').split(",")
        
        for selectedInstance in selectedInstances:
            tempInstance = Instance.objects.get(pk=int(selectedInstance))
            if (tempInstance.status != 5):
                tempInstance.proxy.force_shutdown()
        
        return JsonResponse({'success': True}) 