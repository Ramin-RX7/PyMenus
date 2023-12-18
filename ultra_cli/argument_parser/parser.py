import sys
from types import GenericAlias
from typing import Literal,get_origin,Callable,Any,Union




class Positional:
    def __class_getitem__(cls, item):
        return (cls, item)


class ValidationError(Exception):
    pass

