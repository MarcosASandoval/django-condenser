import mock
from unittest import TestCase
from condenser import Condenser
from django.db import IntegrityError

class CondenserTests(TestCase):

    def setUp(self):
        self.patcher = mock.patch('condenser.get_app')
        self.app_mock = mock.MagicMock()
        self.get_app_mock = self.patcher.start()
        self.get_app_mock.return_value = self.app_mock

    def tearDown(self):
        self.patcher.stop()
        
    def test_condenser_initialize(self):
        """
        Tests that the condenser class initializes properly, setting the instance's
        condensed and canon members properly
        """
        con = Condenser('testapp', 'modela')
        self.get_app_mock.assert_called_with('testapp')

        self.assertEqual(con.app, self.app_mock)
        self.assertEqual(con.model, self.app_mock.modela)

    def test_condenser_get_object(self):
        """
        Tests that the get_object method properly returns the object based on the id passed.
        """
        self.app_mock.modela.objects.get.return_value = mock.sentinel.some_object

        id_str = '1'

        con = Condenser('app', 'modela')
        obj = con.get_object(id_str)
        
        self.app_mock.modela.objects.get.assert_called_with(id=id_str)
        self.assertEqual(obj, mock.sentinel.some_object)

    @mock.patch.object(Condenser, 'get_object')
    def test_condenser_get_condensed_list(self, get_object_mock):
        """
        Tests that the get_condensed_list method properly returns the list of objects
        that will be condensed
        """

        get_object_mock.return_value = 'some'

        condense_list = ['2', '3', '4', '5']
        expected_list = ['some' for i in range(len(condense_list))]

        con = Condenser('app', 'modela')
        condensed = con.get_condensed_list(condense_list)
        
        self.assertEqual(condensed, expected_list)

    def test_condenser_get_condensed_list_without_list_raises_exception(self):
        """
        Tests that the get_condensed_list method raises a TypeError Exception
        when not passed a list as argument
        """
        condense_list = '3'
        con = Condenser('app', 'modela')

        self.assertRaises(TypeError, con.get_condensed_list(condense_list))

    def test_condenser_delete_condensed(self):
        """
        This tests that the condensed objects are deleted
        """
        con = Condenser('app', 'modela')

        obj_mock = mock.MagicMock()
        condensed_list = [obj_mock for i in range(5)]

        con.delete_condensed(condensed_list)

        self.assertEqual(obj_mock.delete.call_count, 5)

    def test_condenser_delete_condensed_raises_exception_without_list(self):
        """
        Test whether the delete_condensed method raises an exception when it's
        not provided with a list
        """
        con = Condenser('app', 'modela')

        self.assertRaises(TypeError, con.delete_condensed('someval'))

    @mock.patch.object(Condenser, 'get_related_objects')
    def test_condenser_move_relations(self, get_related_objects_mock):
        """
        This tests that the relations on the object being condensed (deleted)
        is remapped to the "canonical" object.
        """
        obj_mock = mock.MagicMock()
        da_list = [obj_mock for i in range(5)]
        get_related_objects_mock.return_value = [('related', da_list) for i in range(10)]
        
        canon_mock = mock.MagicMock()
        condensed_mock = mock.MagicMock()

        con = Condenser('app', 'modela')
        con.move_relations(canon_mock, condensed_mock)

        get_related_objects_mock.assert_called_with(condensed_mock)
        self.assertEqual(obj_mock.save.call_count, 50)

    @mock.patch.object(Condenser, 'get_related_objects')
    def test_condenser_move_relations_deletes_object_when_IntegrityError_raised(self, get_related_objects_mock):
        """
        This tests that the move_relations method deletes the object when an IntegrityError
        exception is raised. Going to have to look in to the exceptions that each database
        engine will raise when encountering a duplicate key or unique contraint error
        """
        obj_mock = mock.MagicMock()
        obj_mock.save.side_effect = IntegrityError
        get_related_objects_mock.return_value = [('related', [obj_mock])]
        
        canon_mock = mock.MagicMock()
        condensed_mock = mock.MagicMock()

        con = Condenser('app', 'modela')
        con.move_relations(canon_mock, condensed_mock)
        
        obj_mock.save.assert_called_with()
        obj_mock.delete.assert_called_with()

    def test_condenser_get_related_objects(self):
        """
        Test that we're getting the objects related with the object given
        """
        con = Condenser('app', 'modela')

        related_objects = ['relobj_a', 'relobj_b', 'relobj_c']

        relation_manager_mock = mock.MagicMock()
        relation_manager_mock.get_accessor_name.side_effect = related_objects

        model_mock = mock.MagicMock()
        model_mock._meta.get_all_related_objects.return_value = [
                relation_manager_mock for i in range(len(related_objects))
            ]

        result = con.get_related_objects(model_mock)

        # Assertions
        self.assertEqual(
                relation_manager_mock.get_accessor_name.call_count,
                len(related_objects)
            )

        # assert each related object manager had its all method called
        model_mock.relobj_a.all.assert_called_with()
        model_mock.relobj_b.all.assert_called_with()
        model_mock.relobj_c.all.assert_called_with()

        # create the list we expect to receive
        expected_list = [(
                relation_manager_mock.field.name, getattr(model_mock, x).all()
            ) for x in related_objects]

        self.assertEqual(result, expected_list)
