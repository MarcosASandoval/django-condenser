from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from condenser import get_installed_apps, get_app_models, get_model_fields
import json

def index(request):
    return HttpResponse("Index")

def condense(request):
    return HttpResponse("condense")

def inspector(request):
    if 'app' in request.GET and 'model' in request.GET:
        result = get_model_fields(request.GET['app'], request.GET['model'])
    elif 'app' in request.GET:
        result = get_app_models(request.GET['app'])
    else:
        result = get_installed_apps()
        
    return HttpResponse(json.dumps(result))
