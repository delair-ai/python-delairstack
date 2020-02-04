"""Definitions related to type hints.

"""
import pathlib
import sys

from delairstack.core.resources.resource import Resource

if sys.version_info.minor < 5:
    from unittest.mock import MagicMock

    __inst = MagicMock()
    AnyStr = __inst
    Dict = __inst
    Generator = __inst
    List = __inst
    NamedTuple = __inst
    NewType = __inst
    Optional = __inst
    Sequence = __inst
    Tuple = __inst
    Union = __inst
else:
    # for others to import
    from typing import (AnyStr,
                        Dict,
                        Generator,
                        List,
                        NamedTuple,
                        NewType,
                        Optional,
                        Sequence,
                        Tuple,
                        Union)

AnyPath = NewType('AnyPath', Union[str, pathlib.Path])

ResourceId = NewType('ResourceId', str)

ResourcesWithTotal = NamedTuple('ResourcesWithTotal',
                                [('total', int), ('results', List[Resource])])

SomeResourceIds = NewType('SomeResourceIds',
                          Union[ResourceId, List[ResourceId]])

SomeResources = NewType('SomeResources',
                        Union[Resource, List[Resource]])
