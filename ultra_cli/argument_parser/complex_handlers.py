from types import UnionType,GenericAlias
from typing import get_origin,get_args,_LiteralGenericAlias

from .exceptions import ValidationError



def parse_union(arg_name, arg_type:UnionType, values:tuple):
    types = get_args(arg_type)
    for type in types:
        if type is type(None):
            continue
        try:
            return type(values[0])
        except:
            pass
    raise ValidationError(f"Invalid value for argument `{arg_name}`") from None


def parse_literal(arg_name:str, arg_type:_LiteralGenericAlias, values:tuple):
    acceptables = get_args(arg_type)
    results = []
    for value in values:
        if value not in acceptables:
            raise ValidationError(f"argument `{arg_name}` only accepts one of `{acceptables}`")
        results.append(value)
    return results if len(results) > 1 else results[0]
