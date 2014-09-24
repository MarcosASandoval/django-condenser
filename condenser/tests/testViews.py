from unittest import TestCase
from django.test import RequestFactory
from django.conf import settings
import mock
import json

from condenser import views

class inspectorViewTests(TestCase):

    def setUp(self):
        self.req = RequestFactory()

    @mock.patch('condenser.views.get_installed_apps')
    def test_inspector_view_gets_installed_apps(self, mockget):
        """
        Test that the inspector view returns the correct list of installed apps
        """
        expected_list = ['testapp1', 'testapp2', 'testapp3']
        mockget.return_value = expected_list

        jsonlist = json.dumps(expected_list)

        request = self.req.get('/condenser/inspector')
        response = views.inspector(request)

        mockget.assert_called_with()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, jsonlist)

    @mock.patch('condenser.views.get_app_models')
    def test_inspector_view_gets_app_models(self, mockget):
        """
        Test that the inspector view returns the correct list of models in the app
        based on URL parameters
        """
        expected_list = ['modela', 'modelb', 'modelc']
        mockget.return_value = expected_list

        jsonlist = json.dumps(expected_list)

        request = self.req.get('/condenser/inspector?app=scoreboard')
        response = views.inspector(request)

        mockget.assert_called_with('scoreboard')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, jsonlist)

    @mock.patch('condenser.views.get_model_fields')
    def test_inspector_view_gets_model_fields(self, mockget):
        """
        Tests that the inspector view returns the list of model fields properly
        """
        expected_list = ['id', 'name', 'something']
        mockget.return_value = expected_list

        jsonlist = json.dumps(expected_list)

        request = self.req.get('/condenser/inspector?app=scoreboard&model=modela')
        response = views.inspector(request)

        mockget.assert_called_with(request.GET['app'], request.GET['model'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, jsonlist)

    @mock.patch('condenser.views.serializers')
    @mock.patch('condenser.views.get_model')
    def test_inspector_view_gets_list_of_model_objects(self, get_model_mock, serial_mock):
        """
        Tests that the inspector view returns the correct list of model objects based on the
        URL parameters
        """
        get_model_mock().objects.filter.return_value = 'returnvals'

        request = self.req.get('/condenser/inspector?app=scoreboard&model=modela&field=name&value=testvalue')

        response = views.inspector(request)

        get_model_mock.assert_called_with(request.GET['app'], request.GET['model'])
        get_model_mock().objects.filter.assert_called_with(**{request.GET['field'] + '__contains': request.GET['value']})
        serial_mock.serialize.assert_called_with('json', 'returnvals')

class indexViewTests(TestCase):

    def setUp(self):
        self.req = RequestFactory()

    @mock.patch('condenser.views.render')
    def test_index_view(self, render_mock):
        """
        Tests that the index view calls the render function with the condenser.html
        template as part of the arguments
        """
        request = self.req.get('/condenser')

        response = views.index(request)
        render_mock.assert_called_with(request, 'condenser/index.html')

class condenseViewTests(TestCase):

    def setUp(self):
        self.req = RequestFactory()

    def test_condense_view_without_data(self):
        """
        Tests that the condense view returns the right response when the proper
        parameters aren't passed
        """
        request = self.req.get('/condenser/condense')

        response = views.condense(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'nothing to condense')

    @mock.patch('condenser.views.Condenser')
    def test_condense_calls_condense(self, condenser_mock):
        """
        Tests that the condense view instantiates the condenser class
        """
        expected_response = "Yep, totes condensed"
        mock_instance = condenser_mock.return_value
        mock_instance.result = expected_response

        request = self.req.post(
                'condenser/condense',
                {
                    'canon': '1',
                    'condensed': ['1','2','3','4'],
                    'app': 'app1',
                    'model': 'modela',
                    'delete': True
                }
            )
        response = views.condense(request)

        self.assertEqual(response.status_code, 200)
        condenser_mock.assert_called_with(request.POST['app'], request.POST['model'])
        mock_instance.condense.assert_called_with(
                request.POST['canon'],
                request.POST.getlist('condensed')
            )
        self.assertEqual(response.content, expected_response)

    @mock.patch('condenser.views.Condenser')
    def test_condense_calls_condense_no_delete(self, condenser_mock):
        """
        Tests that the condense view instantiates the condenser class
        """
        expected_response = "Yep. Totes condensed, but not deleted"
        mock_instance = condenser_mock.return_value
        mock_instance.result = expected_response

        request = self.req.post(
                'condenser/condense',
                {
                    'canon': '1',
                    'condensed': ['1','2','3','4'],
                    'app': 'app1',
                    'model': 'modela'
                }
            )
        response = views.condense(request)

        self.assertEqual(response.status_code, 200)
        condenser_mock.assert_called_with(request.POST['app'], request.POST['model'])
        mock_instance.condense_no_delete.assert_called_with(
                request.POST['canon'],
                request.POST.getlist('condensed')
            )
        self.assertEqual(response.content, expected_response)
