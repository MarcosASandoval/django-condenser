from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.core import serializers
from condenser import get_installed_apps, get_app_models, get_model_fields, get_model
from condenser import Condenser
import json

def index(request):
    return render(request, 'condenser/index.html')

# TODO: Run this in a transaction!!!
def condense(request):
    if request.method == 'POST' and 'canon' in request.POST and 'condensed' in request.POST:
        canon = request.POST['canon']
        condensed = request.POST.getlist('condensed')
        con = Condenser(request.POST['app'], request.POST['model'])
        if 'delete' in request.POST:
            con.condense(canon, condensed)
        else:
            con.condense_no_delete(canon, condensed)

    result = con.result
    return HttpResponse(result)

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
