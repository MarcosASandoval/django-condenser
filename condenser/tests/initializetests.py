import sys
from django.test import TestCase
from django.conf import settings
from django.db import models as djmodels
import condenser

class modela(djmodels.Model):
    name = djmodels.CharField('Name', max_length = 20)

class models:
    __path__ = []
    modela = modela

class testapplication1:
    __path__ = []
    models = models


class InitializeTests(TestCase):

    def setUp(self):
        self.apps = [
            'django.contrib.admin',
            'django.contrib.sites',
            'testapplication1',
            'application2',
            'condenser'
        ]

        modela.__module__ = 'testapplication1.models'
        sys.modules['testapplication1'] = testapplication1
        sys.modules['testapplication1.models'] = models

    def test_get_installed_applications_method(self):
        """
        Test that we get the list of installed apps correctly
        """
        
        settings.INSTALLED_APPS = self.apps
        expectedlist = ['testapplication1', 'application2']
        self.assertEquals(
                condenser.get_installed_apps(),
                expectedlist,
                "Did not retrieve list of installed apps properly"
            )

    def test_get_app_models(self):
        """
        Test whether we can get the app's models properly
        """

        settings.INSTALLED_APPS = self.apps
        expectedlist = [('modela', modela)]
        self.assertEquals(
                condenser.get_app_models('testapplication1.models'),
                expectedlist,
                "Did not retrieve list of models properly"
            )

    def test_get_model_fields(self):
        """
        Test whether we can get the model's fields properly
        """

        expectedlist = ['id', 'name']
        self.assertEquals(
                condenser.get_model_fields('testapplication1.models', 'modela'),
                expectedlist,
                "Did not properly retrieve list of fields in model"
            )
