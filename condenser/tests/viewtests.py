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
    def test_inspector_view_calls_condenser_get_installed_apps(self, mockget):
        expected_list = ['testapp1', 'testapp2', 'testapp3']
        mockget.return_value = expected_list

        jsonlist = json.dumps(expected_list)

        request = self.req.get('/condenser/inspector')
        response = views.inspector(request)

        mockget.assert_called_with()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, jsonlist)

    @mock.patch('condenser.views.get_app_models')
    def test_inspector_view_calls_condenser_get_app_models(self, mockget):
        expected_list = ['modela', 'modelb', 'modelc']
        mockget.return_value = expected_list

        jsonlist = json.dumps(expected_list)

        request = self.req.get('/condenser/inspector?app=scoreboard')
        response = views.inspector(request)

        mockget.assert_called_with('scoreboard')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, jsonlist)

    @mock.patch('condenser.views.get_model_fields')
    def test_inspector_view_calls_condenser_get_model_fields(self, mockget):
        expected_list = ['id', 'name', 'something']
        mockget.return_value = expected_list

        jsonlist = json.dumps(expected_list)

        request = self.req.get('/condenser/inspector?app=scoreboard&model=modela')
        response = views.inspector(request)

        mockget.assert_called_with('scoreboard', 'modela')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, jsonlist)

class indexViewTests(TestCase):

    def setUp(self):
        self.req = RequestFactory()

    def test_index_view(self):
        request = self.req.get('/condenser')

        response = views.index(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'Index')

class condenseViewTests(TestCase):

    def setUp(self):
        self.req = RequestFactory()

    def test_condense_view(self):
        request = self.req.get('/condenser/condense')

        response = views.condense(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'condense')

