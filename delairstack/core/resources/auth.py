"""Resources managers related to auth.

"""

from delairstack.apis.provider import Provider


class ShareTokens:
    def __init__(self, *, provider: Provider, **kwargs):
        self._provider = provider
