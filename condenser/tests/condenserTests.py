import mock
from unittest import TestCase
from condenser import Condenser

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
        pass

    def test_condenser_move_relations(self):
        """
        This tests that the relations on the objects being condensed (deleted)
        are remapped to the "canonical" object.
        """
        pass
