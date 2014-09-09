import mock
import condenser
from unittest import TestCase
from django.conf import settings

class InitializeTests(TestCase):

    def setUp(self):
        
        self.mockapp = mock.MagicMock()

        modds = {
                'testapplication1': self.mockapp,
                'testapplication1.models': self.mockapp.models,
            }

        self.modpatcher = mock.patch.dict('sys.modules', modds)
        self.modpatcher.start()

    def tearDown(self):
        self.modpatcher.stop()

    def test_get_installed_applications_method(self):
        """
        Test that we get the list of installed apps correctly
        """
        
        settings.INSTALLED_APPS = [
            'django.contrib.admin',
            'django.contrib.sites',
            'testapplication1',
            'application2',
            'condenser'
        ]
        
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

        # ensure that testapplication1.models.modela returns a class
        p = mock.PropertyMock(return_value=type(self.mockapp.models.modela))
        type(self.mockapp.models).modela = p
        self.mockapp.models.modela.__module__ = 'testapplication1.models'

        expectedlist = [('modela', self.mockapp.models.modela)]
        self.assertEquals(
                condenser.get_app_models('testapplication1.models'),
                expectedlist,
                "Did not retrieve list of models properly"
            )

    def test_get_model_fields(self):
        """
        Test whether we can get the model's fields properly
        """
        
        fields = condenser.get_model_fields('testapplication1.models', 'modela')
        
        # This ensures that modela._meta.get_all_field_names is called
        self.mockapp.models.modela._meta.get_all_field_names.assert_called_with()
