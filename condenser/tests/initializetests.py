import mock
#import sys
import condenser
from django.test import TestCase
from django.conf import settings
from django.db import models as djmodels


class InitializeTests(TestCase):

    def setUp(self):
        settings.INSTALLED_APPS = [
            'django.contrib.admin',
            'django.contrib.sites',
            'testapplication1',
            'application2',
            'condenser'
        ]
        
        self.mockapp = mock.MagicMock()
        p = mock.PropertyMock(return_value=type(self.mockapp.models.modela))
        type(self.mockapp.models).modela = p
        self.mockapp.models.modela.__module__ = 'testapplication1.models'

        modds = {
                'testapplication1': self.mockapp,
                'testapplication1.models': self.mockapp.models,
                'testapplication1.models.modela': self.mockapp.models.modela
            }


        self.modpatcher = mock.patch.dict('sys.modules', modds)
        self.modpatcher.start()

    def tearDown(self):
        self.modpatcher.stop()

    def test_get_installed_applications_method(self):
        """
        Test that we get the list of installed apps correctly
        """
        
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

        expectedlist = [('modela', self.mockapp.models.modela)]
        self.assertEquals(
                condenser.get_app_models('testapplication1.models'),
                expectedlist,
                "Did not retrieve list of models properly"
            )

    #@mock.patch('testapplication1.models')
    def test_get_model_fields(self):
        """
        Test whether we can get the model's fields properly
        """
        #print mocky._meta
        fields = condenser.get_model_fields('testapplication1.models', 'modela')

#        expectedlist = ['id', 'name']
#        self.assertEquals(
#                condenser.get_model_fields('testapplication1.models', 'modela'),
#                expectedlist,
#                "Did not properly retrieve list of fields in model"
#            )
