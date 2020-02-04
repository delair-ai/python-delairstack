import os.path
import json

from delairstack.core.config import ConnectionConfig
from tests.delairstacktest import DelairStackTestBase
from unittest import mock
from delairstack.core.utils.filehelper import read_file

DEFAULT_MOCK_CONTENT = {
                'password': 'default password',
                'user': 'default user',
                'secret': 'default secret',
                'url': 'default url',
                'connection': {
                    'max_retries': 1,
                    'disable_ssl_certificate': True
                }

            }


class TestConnectionConfig(DelairStackTestBase):
    """Tests for connection configuration.

    """
    def test_default_config(self):
        """Test default configuration."""
        conf = ConnectionConfig()
        self.assertEqual(conf.url, 'https://www.delair.ai')
        self.assertEqual(conf.connection['disable_ssl_certificate'], True)

    def test_complete_custom_config(self):
        """Test loading a complete custom configuration."""
        conf_path = os.path.join(os.path.dirname(__file__),
                                 'config-complete-connection.json')
        conf = ConnectionConfig(file_path=conf_path)
        self.assertEqual(conf.user, 'user')
        self.assertEqual(conf.password, 'password')
        self.assertEqual(conf.secret, 'secret')
        self.assertEqual(conf.url, 'https://www.delair.ai')
        self.assertEqual(conf.connection['max_retries'], 10)
        self.assertEqual(conf.connection['disable_ssl_certificate'], False)

    def test_partial_custom_config(self):
        """Test loading a partial custom configuration."""
        conf_path = os.path.join(os.path.dirname(__file__),
                                 'config-partial-connection.json')
        conf = ConnectionConfig(file_path=conf_path)

        self.assertEqual(conf.user, 'user')
        self.assertEqual(conf.connection['disable_ssl_certificate'], False)

    def test_override_default_config(self):
        """Test overloading default configuration with keywords arguments."""
        with mock.patch('delairstack.core.config.read_file') as mock_read_file:
            mock_read_file.return_value = json.dumps(DEFAULT_MOCK_CONTENT)
            conf = ConnectionConfig(user='other')
            self.assertEqual(conf.user, 'other')
            self.assertEqual(conf.url, 'https://www.delair.ai')
            self.assertEqual(
                conf.connection['disable_ssl_certificate'], True)

    def test_override_custom_config(self):
        """Test overloading custom configuration with keywords arguments."""
        conf_path = os.path.join(os.path.dirname(__file__),
                                 'config-partial-connection.json')
        conf = ConnectionConfig(file_path=conf_path, user='username')
        self.assertEqual(conf.user, 'username')
        self.assertEqual(conf.url, 'https://www.delair.ai')
        self.assertEqual(conf.connection['disable_ssl_certificate'], False)
