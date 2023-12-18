import sys
from types import GenericAlias
from typing import Literal,get_origin,Callable,Any,Union




class Positional:
    def __class_getitem__(cls, item):
        return (cls, item)


class ValidationError(Exception):
    pass




class Option:
    def __init__(self,
        name : str,
        validator : Callable,
        abrev : bool = True,
        positional : bool = False,
        help : str = "",
        default : Any = ...,
        maximum : int = 1
      ):
        self.name = name
        self.validator = validator
        self.abrev = abrev
        self.positional = positional
        self.help = help
        self.default = default
        self.maximum = maximum
        self.required = True if default is Ellipsis else False


    def parse(self, *values):
        if len(values) > self.maximum:
            raise ValidationError(f"You can use `{self.name}` option only `{self.maximum}` times.")

        if isinstance(self.validator, GenericAlias):
            return

        elif isinstance(self.validator, Union):
            return

        elif isinstance(self.validator, Literal):
            return

        else:
            validator = self.validator

        if self.required:
            result = values #or self.default
            if result is None:
                raise ValidationError(f"`{self.name}` option is required")

        if self.validator not in (list,tuple,set):
            for value in values:
                if isinstance(value, (list,set,tuple)):
                    raise ValidationError(f"`{self.name}` option must have single argument")

        if self.validator is bool:
            if self.default in (Ellipsis,False):
                return True
            return False

        try:
            if len(values) == 1:
                return validator(values[0])
            else:
                return [validator(value) for value in values]
        except Exception as e:
            raise ValidationError(str(e)) from None


    def __repr__(self):
        # return f"{self.__class__.__name__}({self.name})"
        return f"{self.name}"



class ArgumentParser:
    class _config:
        name = ""
        description = ""
        abrev = True

    def __init__(self):
        self.args : dict[str,Option] = {}
        args = self.__annotations__
        for arg_name,arg_type in args.items():
            if hasattr(self, arg_name) and isinstance(getattr(self, arg_name), Option):
                self.args.append(getattr(self, arg_name))
                continue
            self.args[arg_name] = Option(
                name = arg_name,
                validator = arg_type,
                abrev = self._config.abrev,
                positional = True if get_origin(arg_type)==Positional else False
            )

    def _validate(self, args):
