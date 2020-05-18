"""Resource manager for products.

"""

from datetime import datetime

from delairstack.apis.provider import Provider


class Products:
    _name = 'product'

    def __init__(self, *, provider=Provider, **kwargs):
        self._provider = provider


class ProductLog:
    def __init__(self, *, timestamp: datetime, record: dict):
        self.timestamp = timestamp
        self.record = record
