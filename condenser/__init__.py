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
    module = importlib.import_module(app)
    models_list = inspect.getmembers(module,
            # Not a fan of having to compare the module name to the parameter 'app',
            # but the import_module method will uncover the true namespace of the module,
            # breaking our unit tests. Otherwise we could replace app with module.__name__
            lambda member: inspect.isclass(member) and member.__module__ == app
        )

    return models_list

def get_model_fields(app, model):
    app = importlib.import_module(app)
    model = getattr(app, model)
    fields = model._meta.get_all_field_names()
    return fields
