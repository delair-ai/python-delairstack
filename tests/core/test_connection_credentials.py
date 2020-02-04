import base64

from delairstack.core.connection.credentials import (ClientCredentials,
                                                     UserCredentials)

from tests.delairstacktest import DelairStackTestBase


class TestClientCredentials(DelairStackTestBase):
    """Tests for client credentials.

    """
    def test_initialization(self):
        """Test client credentials initialization."""
        creds = ClientCredentials('5aabc6df52e3ea3a3bd57a47', 'thesecret')
        self.assertDictEqual(creds.data, {'grant_type': 'client_credentials'})
        decoded_secret = base64.b64decode(creds.encoded_secret).decode()
        client_id, secret = decoded_secret.split(':')
        self.assertEqual(client_id, '5aabc6df52e3ea3a3bd57a47')
        self.assertEqual(secret, 'thesecret')


class TestUserCredentials(DelairStackTestBase):
    """Tests for user credentials.

    """
    def test_initialization(self):
        """Test user credentials initialization."""
        creds = UserCredentials('tristram', 'thepassword')
        self.assertDictEqual(creds.data,
                             {'grant_type': 'password',
                              'username': 'tristram',
                              'password': 'thepassword'})
        decoded_secret = base64.b64decode(creds.encoded_secret).decode()
        client_id, secret = decoded_secret.split(':')
        self.assertEqual(client_id, 'abc123')
        self.assertEqual(secret, 'ssh-secret')
