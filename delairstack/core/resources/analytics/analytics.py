"""Resource manager for Analytics.

"""

from delairstack.apis.provider import Provider


class Analytics:
    _name = 'analytic'

    def __init__(self, *, provider=Provider, **kwargs):
        self._provider = provider
