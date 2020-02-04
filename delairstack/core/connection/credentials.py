"""Connection credentials.

"""

import base64


class Credentials():
    """Base class for connection credentials.

    """
    def __init__(self, client_id, secret, *, data):
        self._data = data
        secret = '{}:{}'.format(client_id, secret)
        self._encoded_secret = base64.b64encode(secret.encode()).decode()

    @property
    def encoded_secret(self):
        return self._encoded_secret

    @property
    def data(self):
        return self._data


class ClientCredentials(Credentials):
    """Client credentials.

    """
    def __init__(self, client_id, secret):
        super().__init__(client_id, secret,
                         data={'grant_type': 'client_credentials'})


class UserCredentials(Credentials):
    """User credentials.

    """
    __sdk_client_id = 'abc123'
    __secret = 'ssh-secret'

    def __init__(self, user, password, *, client_id=None, secret=None, domain=None):
        client_id = client_id or self.__sdk_client_id
        secret = secret or self.__secret
        data = {'grant_type': 'password',
                'username': user,
                'password': password}
        if domain:
            data.update({'scope': 'domain:{}'.format(domain)})
        super().__init__(client_id,
                         secret,
                         data=data)
