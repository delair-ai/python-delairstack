"""Resource manager related to credentials.

"""

from delairstack.apis.provider import Provider


class Credentials():
    _name = 'credentials'

    def __init__(self, *, provider: Provider, **kwargs):
        self._provider = provider
