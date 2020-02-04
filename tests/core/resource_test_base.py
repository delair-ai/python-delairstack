import os
from unittest.mock import patch

from delairstack import DelairStackSDK
from tests.delairstacktest import DelairStackTestBase
from delairstack.core.connection.token import TokenManager


class ResourcesTestBase(DelairStackTestBase):

    @classmethod
    def setUpClass(cls):
        with patch('delairstack.core.connection.token.TokenManager.renew_token') as mock:
            cls.sdk = DelairStackSDK(config_path=cls.get_absolute_path("./config-test.json"))

    @staticmethod
    def get_absolute_path(file_path):
        return os.path.join(os.path.dirname(__file__), file_path)
