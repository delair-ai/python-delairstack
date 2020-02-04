import copy

from delairstack.core.config import ConnectionConfig
from delairstack.core.errors import ConfigError
from delairstack.core.utils.utils import (new_instance, flatten_dict, find, dict_merge)
from tests.delairstacktest import DelairStackTestBase


d1 = {
    'a': {
        'b': {
            'c': 'd'
            }
        }
    }

d2 = {
    'a': {
        'b': {
            'c': 'd',
            'e': 'f'
            }
        }
    }

d3 = {
    'a': {
        'b': {
            'c': 'g'
            }
        }
    }


class TestUtils(DelairStackTestBase):
    """Tests for utilities.

    """

    def test_new_instance_existing(self):
        """Test instance creation for existing module and class."""
        instance = new_instance('delairstack.core.config', 'ConnectionConfig')
        self.assertNotEqual(instance, None)
        self.assertIsInstance(instance, ConnectionConfig)

    def test_new_instance_non_existing(self):
        """Test instance creation for non existing module or class."""
        with self.assertRaises(ConfigError):
            new_instance('blabla', class_name=None)

        with self.assertRaises(ConfigError):
            new_instance(module_path=None, class_name=None)

        with self.assertRaises(ConfigError):
            new_instance('delairstack.core.config', 'FakeClass')

        with self.assertRaises(ConfigError):
            new_instance('delairstack.fake_module', 'TestClass')

    def test_flatten(self):
        res = flatten_dict(copy.deepcopy(d1))
        self.assertEqual(res['a.b.c'], 'd')

        d = {}
        res = flatten_dict(d)
        self.assertEqual(len(res), 0)

        d = {
            'a': 'b'
            }

        res = flatten_dict(d)
        self.assertEqual(res['a'], 'b')

    def test_find(self):
        self.assertEqual(find(copy.deepcopy(d1), 'a.b.c'), 'd')

    def test_merge_dict(self):
        res = dict_merge(copy.deepcopy(d1), copy.deepcopy(d2))
        self.assertEqual(res, {'a': {'b': {'c': 'd', 'e': 'f'}}})

    def test_merge_dict_in_place(self):
        h = copy.deepcopy(d1)
        dict_merge(h, {'a': {'y':2}})
        self.assertEqual(h, {'a': {'b': {'c': 'd'}, 'y': 2}})

    def test_merge_dict_with_add_keys(self):
        res = dict_merge(copy.deepcopy(d1), copy.deepcopy(d2), add_keys=False)
        self.assertEqual(res, {'a': {'b': {'c': 'd'}}})
