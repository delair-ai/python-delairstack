"""Tests related to connections.

"""

import json
import unittest
from unittest.mock import MagicMock, patch

import urllib3
from urllib3.util.retry import Retry

import delairstack
from delairstack.core.connection.connection import (Connection,
                                                    AsyncConnection, )
from delairstack.core.connection.credentials import ClientCredentials
from delairstack.core.connection.token import TokenManager
from delairstack.core.errors import ResponseError
from tests.delairstacktest import DelairStackTestBase


@patch.object(urllib3.PoolManager, 'request')
class TestConnection(DelairStackTestBase):
    """Tests synchronous connection.

    """

    @patch('delairstack.core.connection.token.TokenManager.renew_token')
    def setUp(self, mock):
        creds = ClientCredentials(client_id='fake_client_id',
                                  secret='fake_client_secret')
        conn_opts = {
            'base_url': 'https://www.delair.ai',
            'credentials': creds}
        self.conn = Connection(**conn_opts)

    def test_post(self, mocked_req):
        """Test POST with different arguments."""
        mocked_req.return_value = MagicMock(status=200, data='received data')

        resp_data = self.conn.post('/path')
        self.assertEqual(resp_data, 'received data')
        mocked_req.assert_called_once()
        call_args = mocked_req.call_args[1]
        del call_args['retries']
        self.assertDictEqual(call_args, {
            'body': {},
            'headers': {'User-Agent': 'python-delairstack/{}'.format(delairstack.__version__)},
            'method': 'POST',
            'timeout': 30.0,
            'preload_content': True,
            'url': 'https://www.delair.ai/path'})

        mocked_req.clear()
        mocked_req.return_value.data = '{"key": "value"}'.encode('utf-8')
        resp_data = self.conn.post('other', data='data to send',
                                   headers={'Custom-Header': 'Test'},
                                   timeout=15.0, as_json=True)
        self.assertDictEqual(resp_data, {'key': 'value'})
        self.assertEqual(mocked_req.call_count, 2)
        call_args = mocked_req.call_args[1]
        del call_args['retries']
        self.assertDictEqual(call_args, {
            'body': 'data to send',
            'headers': {'Custom-Header': 'Test', 'User-Agent': 'python-delairstack/{}'.format(delairstack.__version__)},
            'method': 'POST',
            'preload_content': True,
            'timeout': 15.0,
            'url': 'https://www.delair.ai/other'})

    def test_post_failure(self, mocked_req):
        """Test POST with failure."""
        mocked_req.return_value = MagicMock(status=500, data='received data')

        with self.assertRaises(ResponseError):
            self.conn.post('/path')

        mocked_req.assert_called_once()

    def test_get(self, mocked_req):
        """Test GET."""
        mocked_req.return_value = MagicMock(status=200, data='received data')

        resp_data = self.conn.get('/path')
        self.assertEqual(resp_data, 'received data')
        mocked_req.assert_called_once()
        call_args = mocked_req.call_args[1]
        del call_args['retries']
        self.assertDictEqual(call_args, {
            'headers': {'User-Agent': 'python-delairstack/{}'.format(delairstack.__version__)},
            'method': 'GET',
            'timeout': 30.0,
            'preload_content': True,
            'url': 'https://www.delair.ai/path'})

        mocked_req.clear()
        mocked_req.return_value.data = '{"key": "value"}'.encode('utf-8')
        resp_data = self.conn.get('other',
                                  headers={'Custom-Header': 'Test'},
                                  timeout=15.0, as_json=True)
        self.assertDictEqual(resp_data, {'key': 'value'})
        self.assertEqual(mocked_req.call_count, 2)
        call_args = mocked_req.call_args[1]
        del call_args['retries']
        self.assertDictEqual(call_args, {
            'headers': {'Custom-Header': 'Test', 'User-Agent': 'python-delairstack/{}'.format(delairstack.__version__)},
            'method': 'GET',
            'timeout': 15.0,
            'preload_content': True,
            'url': 'https://www.delair.ai/other'})

    def test_get_failure(self, mocked_req):
        """Test GET with failure."""
        mocked_req.return_value = MagicMock(status=500, data='received data')

        with self.assertRaises(ResponseError):
            self.conn.get('/path')

        mocked_req.assert_called_once()

    def test_get_with_expired_token(self, mocked_req):
        """Test GET with expired token."""
        token_post_resp = {
            'access_token': 'y77ceIHcPu2RKHo9clekkG8B',
            'expires_in': 14400,
            'refresh_token': '0PPCsHkBesbVC2FJpV8eqaXB',
            'token_type': 'Bearer'}
        values = [MagicMock(status=401, data=''),
                  MagicMock(status=200,
                            data=json.dumps(token_post_resp).encode('utf-8')),
                  MagicMock(status=200, data='received data')]
        mocked_req.side_effect = values

        resp_data = self.conn.get('/path')
        self.assertEqual(resp_data, 'received data')
        self.assertEqual(mocked_req.call_count, 3)

    def test_lazy_get(self, mocked_req):
        """Test lazy GET."""
        mocked_req.return_value = MagicMock(status=200, data='received data')
        self.conn.get('/path', preload_content=False)
        mocked_req.assert_called_once()
        call_args = mocked_req.call_args[1]
        del call_args['retries']
        self.assertDictEqual(call_args, {
            'headers': {'User-Agent': 'python-delairstack/{}'.format(delairstack.__version__)},
            'method': 'GET',
            'preload_content': False,
            'timeout': 30.0,
            'url': 'https://www.delair.ai/path'})

    def test_put(self, mocked_req):
        """Test PUT."""
        mocked_req.return_value = MagicMock(status=200, data='received data')

        resp_data = self.conn.put('/path')
        self.assertEqual(resp_data, 'received data')
        mocked_req.assert_called_once()
        call_args = mocked_req.call_args[1]
        del call_args['retries']
        self.assertDictEqual(call_args, {
            'body': {},
            'headers': {'User-Agent': 'python-delairstack/{}'.format(delairstack.__version__)},
            'method': 'PUT',
            'timeout': 30.0,
            'preload_content': True,
            'url': 'https://www.delair.ai/path'})

        mocked_req.clear()
        mocked_req.return_value.data = '{"key": "value"}'.encode('utf-8')
        resp_data = self.conn.put('other', data='data to send',
                                  headers={'Custom-Header': 'Test'},
                                  timeout=15.0, as_json=True)
        self.assertDictEqual(resp_data, {'key': 'value'})
        self.assertEqual(mocked_req.call_count, 2)
        call_args = mocked_req.call_args[1]
        del call_args['retries']
        self.assertDictEqual(call_args, {
            'body': 'data to send',
            'headers': {'Custom-Header': 'Test', 'User-Agent': 'python-delairstack/{}'.format(delairstack.__version__)},
            'method': 'PUT',
            'timeout': 15.0,
            'preload_content': True,
            'url': 'https://www.delair.ai/other'})

    def test_put_failure(self, mocked_req):
        """Test PUT with failure."""
        mocked_req.return_value = MagicMock(status=500, data='received data')

        with self.assertRaises(ResponseError):
            self.conn.put('/path')

        mocked_req.assert_called_once()

    def test_delete(self, mocked_req):
        """Test delete."""
        mocked_req.return_value = MagicMock(status=200, data='received data')

        resp_data = self.conn.delete('/path')
        self.assertEqual(resp_data, 'received data')
        mocked_req.assert_called_once()
        call_args = mocked_req.call_args[1]
        del call_args['retries']
        self.assertDictEqual(call_args, {
            'body': {},
            'headers': {'User-Agent': 'python-delairstack/{}'.format(delairstack.__version__)},
            'method': 'DELETE',
            'timeout': 30.0,
            'url': 'https://www.delair.ai/path'})

        mocked_req.clear()
        mocked_req.return_value.data = '{"key": "value"}'.encode('utf-8')
        resp_data = self.conn.delete('other', data='data to send',
                                     headers={'Custom-Header': 'Test'},
                                     timeout=15.0, as_json=True)
        self.assertDictEqual(resp_data, {'key': 'value'})
        self.assertEqual(mocked_req.call_count, 2)
        call_args = mocked_req.call_args[1]
        del call_args['retries']
        self.assertDictEqual(call_args, {
            'body': 'data to send',
            'headers': {'Custom-Header': 'Test', 'User-Agent': 'python-delairstack/{}'.format(delairstack.__version__)},
            'method': 'DELETE',
            'timeout': 15.0,
            'url': 'https://www.delair.ai/other'})

    def test_delete_failure(self, mocked_req):
        """Test DELETE with failure."""
        mocked_req.return_value = MagicMock(status=500)

        with self.assertRaises(ResponseError):
            self.conn.delete('/path')

        mocked_req.assert_called_once()


@unittest.skip('Work in progress...')
@patch.object(urllib3.PoolManager, 'request')
@patch('requests_futures.sessions.FuturesSession', autospec=True)
class TestAsynchronousConnection(DelairStackTestBase):
    """Tests asynchronous connection.

    """

    @patch('delairstack.core.connection.token.TokenManager.renew_token')
    def setUp(self, mock):
        base_url = 'https://localhost'
        creds = ClientCredentials(client_id='fake_client_id',
                                  secret='fake_client_secret')
        token_mngr = TokenManager(base_url, creds,
                                  disable_ssl_certificate=True)
        conn_opts = {
            'base_url': base_url,
            'token_manager': token_mngr}
        self.conn = AsyncConnection(**conn_opts)

    def test_put(self, mocked_session, mocked_req):
        """Test PUT."""
        mocked_req.return_value = MagicMock(status=200, data='received data')

        aresp = self.conn.put('/path')
        resp = aresp.result()
        self.assertEqual(resp.content, 'received data')
        mocked_req.assert_called_once()

        call_args = mocked_req.call_args[1]
        del call_args['retries']
        self.assertDictEqual(call_args, {
            'body': {},
            'headers': {'User-Agent': 'python-delairstack/{}'.format(delairstack.__version__)},
            'method': 'PUT',
            'timeout': 30.0,
            'url': 'https://www.delair.ai/path'})

    def test_put_failure(self, mocked_session, mocked_req):
        """Test PUT with failure."""
        mocked_req.return_value = MagicMock(status=200, data='received data')

        aresp = self.conn.put('/path')
        resp = aresp.result()
        self.assertEqual(resp.content, 'received data')
        mocked_req.assert_called_once()
