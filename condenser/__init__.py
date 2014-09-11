from django.conf import settings
import importlib
import inspect

def get_installed_apps():
    """
    Grabs the list of installed apps and returns the apps that don't
    belong to django nor the condenser app
    """
    newlist = []
    for app in settings.INSTALLED_APPS:
        if not app.startswith('django') and app != 'condenser':
            newlist.append(app)
    return newlist

def get_app_models(app):
    """
    Imports the app that is passed as parameter
    returns list of tuples (MODELNAME, MODELCLASS)
    """
    if not app.endswith('.models'):
        app += '.models'
    
    module = importlib.import_module(app)
    models_list = []
    for member in inspect.getmembers(
            module,
            lambda member: inspect.isclass(member) and member.__module__ == app
        ):
        models_list.append(member[0])

    return models_list

def get_model_fields(app, model):
    if not app.endswith('.models'):
        app += '.models'
    
    app = importlib.import_module(app)
    model = getattr(app, model)
    fields = model._meta.get_all_field_names()
    return fields
