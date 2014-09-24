from django.conf import settings
from django.db.models import get_app
from django.db import IntegrityError
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

class Condenser:
    result = "Nothing condensed"
    # TODO: Add result member that will be set with the outcome of the condense methods
    def __init__(self, app, model):
        self.app = get_app(app)
        self.model = getattr(self.app, model)

    def get_object(self, obj_id):
        return self.model.objects.get(id=obj_id)

    def get_condensed_list(self, condensed):
        condensed_list = []
        try:
            if type(condensed) is not list:
                raise TypeError('Expected a list')
        except TypeError as e:
            #print e.message
            pass

        for id in condensed:
            obj = self.get_object(id)
            condensed_list.append(obj)

        return condensed_list

    def get_related_objects(self, model):
        related_objects = []
        for relation_manager in model._meta.get_all_related_objects():
            relation_accessor = relation_manager.get_accessor_name()

            related_objects.append((
                    relation_manager.field.name,
                    getattr(model, relation_accessor).all()
                ))

        return related_objects

    def delete_condensed(self, condensed):
        try:
            if type(condensed) is not list:
                raise TypeError("Expected a list")

            for obj in condensed:
                obj.delete()
        except TypeError as e:
            pass

    def move_relations(self, canon, condensed):
        """
        Moves the related objects from the condensed object to the canon object. If the
        related object violates a unique_together constraint when its relationship is changed
        it gets deleted. This is found by catching an IntegrityError exception while calling
        the object's save method.

        TODO: ensure that all DB engines raise an IntegrityError exception when encountering
        a unique or duplicate constraint error.
        """
        related_objects = self.get_related_objects(condensed)

        for field, objs in related_objects:
            for obj in objs:
                setattr(obj, field, canon)
                try:
                    obj.save()
                except IntegrityError as e:
                    obj.delete()

    def move_relations_multiple(self, canon, condensed_list):
        for obj in condensed_list:
            self.move_relations(canon, obj)

    def condense(self, canon_id, condensed_ids):
        # TODO: raise exceptions when needed
        try:
            self.condense_no_delete(canon_id, condensed_ids)

            condensed = self.get_condensed_list(condensed_ids)
            self.delete_condensed(condensed)
            self.result = "Successfully condensed objects"
        except Exception as e:
            self.result = e.message

    def condense_no_delete(self, canon_id, condensed_ids):
        # TODO: raise exceptions when needed
        try:
            canon = self.get_object(canon_id)
            condensed = self.get_condensed_list(condensed_ids)
            self.move_relations_multiple(canon, condensed)
            self.result = "Successfully condensed objects"
        except Exception as e:
            self.result = e.message
