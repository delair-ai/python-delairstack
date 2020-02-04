"""Resource manager for datasets.

"""

from delairstack.apis.provider import Provider


class Datasets():
    _name = 'dataset'

    def __init__(self, *, provider: Provider, **kwargs):
        self._provider = provider
