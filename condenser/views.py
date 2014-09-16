from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.core import serializers
from condenser import get_installed_apps, get_app_models, get_model_fields, get_model
import json

def index(request):
    return render(request, 'condenser/index.html')

def condense(request):
    if request.method == 'POST' and 'canon' in request.POST and 'condense' in request.POST:
        canon = request.POST['canon']
        condense = request.POST.getlist('condense')
    else:
        stuff = 'nothing to condense'
    return HttpResponse(stuff)

def inspector(request):
    if 'app' in request.GET and 'model' in request.GET and 'field' in request.GET and 'value' in request.GET:
        model = get_model(request.GET['app'], request.GET['model'])
        objs = model.objects.filter(**{request.GET['field'] + '__contains': request.GET['value']})
        result = serializers.serialize('json', objs)
    elif 'app' in request.GET and 'model' in request.GET:
        result = json.dumps(get_model_fields(request.GET['app'], request.GET['model']))
    elif 'app' in request.GET:
        result = json.dumps(get_app_models(request.GET['app']))
    else:
        result = json.dumps(get_installed_apps())
        
    return HttpResponse(result)
