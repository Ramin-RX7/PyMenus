from types import UnionType
from typing import get_args



def check_none_default(arg_type):
    if isinstance(arg_type, UnionType):
        if type(None) in get_args(arg_type):
            return True
    return False


def clean_class_dict(cls):
    return {k:v for k,v in cls.__dict__.items() if not k.startswith("__")}
