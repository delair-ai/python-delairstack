import json

from delairstack.core.errors import ImmutableAttribute
from delairstack.core.resources.resource import Resource
from delairstack.core.resources.resources_manager_base import ResourcesManagerBase
from tests.delairstacktest import DelairStackTestBase

A_USER_DESC = \
    """
    {"_id":"5aa7f7fd8e329e5d1858ee7e",
     "company":"59aaf4f9f96a310007fdf1af",
     "profile":"user",
     "username":"gustave.eiffel@example.com",
     "displayName":"Gustave Eiffel",
     "status":"connected",
     "dateFormat":"MM/dd/yyyy",
     "marketingEmail":false,
     "eula":{"approvalDate":"2018-03-16T08:35:44.314Z",
             "version":1},
     "units":"metric",
     "companyRole":"user",
     "country":"FRA",
     "language":"en-US",
     "companies":[],
     "segmentation":"pro",
     "scope":{"projects":{"5b4f46a2c41b427c5c563a58":["6666"],
                          "5b4f44b8f107e6664d55cace":["6666"],
                          "5b3cd457c158043a631265a6":["6666"],
                          "5b14fb8ef75c0f393be0d33a":["6666"],
                          "5ad917df29f31a4429d0bac4":["6666"],
                          "5accbec40710ce72820b855c":["6666"],
                          "5abcb2cf63734d7e9a6a915c":["6666"],
                          "5ab50a94d1815b72237474d9":["6666"],
                          "5ac78a2c2c766e116367dc12":["6666"],
                          "5ad46704fbd98f018eb9e20f":["6666"],
                          "5ae1d3babc400944eadc7ffd":["6666"],
                          "5b2b733f80015606cb55bcd0":["6666"],
                          "5b4f437f9d6a2261afd791f5":["6666"],
                          "5b4f45499d6a2261afd792d6":["6666"],
                          "5b4f46af9d6a2261afd79382":["6666"]}},
     "created":"2018-03-13T16:10:37.529Z",
     "email":"gustave.eiffel@example.com",
     "lastName":"Eiffel",
     "firstName":"Gustave"}
    """


class TestResourceBase(DelairStackTestBase):
    """Tests for resources base class.

    """

    def setUp(self):
        self.user_desc = json.loads(A_USER_DESC)

    def test_initialization(self):
        """Test resource initialization."""
        r = Resource('5a4cb0d2c6d4f00007e90e07', desc=self.user_desc)
        self.assertEqual(r.id, '5a4cb0d2c6d4f00007e90e07')

        with self.assertRaises(AttributeError):
            r.fake_attribute

        with self.assertRaises(ImmutableAttribute):
            r.id = 'acb04dc6d42f0000e9700e4a'

        self.assertCountEqual(dir(r), ['_id', 'companies', 'company', 'companyRole',
                                       'country', 'created', 'dateFormat', 'displayName',
                                       'email', 'eula', 'firstName', 'id', 'language',
                                       'lastName', 'marketingEmail', 'profile', 'scope',
                                       'segmentation', 'status', 'units', 'username'])

    def test_setattr(self):
        """Test setting resource attribute."""
        r = Resource('5a4cb0d2c6d4f00007e90e07', desc=self.user_desc)
        self.assertEqual(r.lastName, 'Eiffel')

        r.lastName = 'Courbet'
        self.assertEqual(r.lastName, 'Courbet')

        r.lastName = 'Choquet'
        self.assertEqual(r.lastName, 'Choquet')

        r.email = 'gustave.choquet@example.com'
        self.assertEqual(r.lastName, 'Choquet')

        r.fake_attribute = 'value'
        self.assertEqual(r.fake_attribute, 'value')

    def test_str(self):
        rmb = ResourcesManagerBase(provider=None)
        rmb._name = "unit test name"

        r = Resource('5a4cb0d2c6d4f00007e90e07', desc=self.user_desc, manager=rmb)

        self.assertEqual(repr(r),
                         '<delairstack.core.resources.resource.Resource with id 5a4cb0d2c6d4f00007e90e07 (unit test name)>')

        r = Resource('5a4cb0d2c6d4f00007e90e07', desc=self.user_desc, manager=None)

        self.assertEqual(repr(r),
                         '<delairstack.core.resources.resource.Resource with id 5a4cb0d2c6d4f00007e90e07>')

        r = Resource('', desc=self.user_desc, manager=None)

        self.assertTrue(repr(r).startswith('<delairstack.core.resources.resource.Resource object at'))

        r = Resource('', desc=self.user_desc, manager=rmb)

        self.assertTrue(repr(r).startswith('<delairstack.core.resources.resource.Resource object at'))