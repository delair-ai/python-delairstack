import json
from unittest import mock

import delairstack
from delairstack.core.config import ConnectionConfig
from tests.core.resource_test_base import ResourcesTestBase

DEFAULT_MOCK_CONTENT = {'url': 'some url',
                        'connection': {
                            'max_retries': 1,
                            'disable_ssl_certificate': True}}


class TestSDK(ResourcesTestBase):
    def test_resource_attributes(self):
        self.assertIsInstance(self.sdk.missions,
                              delairstack.apis.client.projectmngt.missionsimpl.MissionsImpl)

        attrs = dir(self.sdk)
        self.assertIn('annotations',  attrs)
        self.assertIn('flights', attrs)
        self.assertIn('missions', attrs)
        self.assertIn('projects', attrs)
        self.assertIn('datasets', attrs)

    @mock.patch('delairstack.core.config.read_file')
    def test_missing_url(self, mock_read_file):
        mock_read_file.return_value = json.dumps({})
        with self.assertRaises(delairstack.core.errors.ConfigError):
            delairstack.DelairStackSDK()

    @mock.patch('delairstack.core.config.read_file')
    def test_missing_credentials(self, mock_read_file):
        mock_read_file.return_value = json.dumps({'url': 'some url'})
        with self.assertRaises(delairstack.core.errors.ConfigError):
            delairstack.DelairStackSDK()

    @mock.patch('delairstack.core.config.read_file')
    def test_wrong_config(self, mock_read_file):
        mock_read_file.return_value = '{"content":"content"}'
        with self.assertRaises(Exception):
            delairstack.DelairStackSDK(user='username', password='password')

    @mock.patch('delairstack.core.connection.token.TokenManager.renew_token')
    def test_renew_token_at_init(self, mock):
        delairstack.DelairStackSDK(user='username', password='password')
        self.assertTrue(mock.called)
