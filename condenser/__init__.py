from django.conf import settings
from django.db.models import get_app
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
    """
    if not app.endswith('.models'):
        appmodels = app + '.models'

    module = get_app(app)

    models_list = []
    for member in inspect.getmembers(
            module,
            lambda member: inspect.isclass(member) and member.__module__ == appmodels
        ):
        models_list.append(member[0])

    return models_list

def get_model_fields(app, model):
    model = get_model(app, model)
    fields = model._meta.get_all_field_names()
    return fields

def get_model(app, model):
    module = get_app(app)
    model = getattr(module, model)
    return model

class condenser:
    
    def __init__(self, app, model):
        self.app = get_app(app)
        self.model = getattr(self.app, model)

    def set_canon(self, canon_id):
        pass

    def set_condensed(self, condensed):
        pass
