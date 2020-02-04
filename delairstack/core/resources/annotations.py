"""Resource manager related to annotations.

"""

from delairstack.apis.provider import Provider


class Annotations():
    _name = 'annotations'

    def __init__(self, *, provider: Provider, **kwargs):
        self._provider = provider
