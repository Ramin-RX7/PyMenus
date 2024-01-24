import sys
from types import GenericAlias,UnionType
from typing import get_origin,Callable,Any,_LiteralGenericAlias, get_args

from .exceptions import ValidationError
from .complex_handlers import parse_union,parse_literal



class Positional:
    def __class_getitem__(cls, item):
        return GenericAlias(cls, item)






def check_none_default(arg_type):
    if isinstance(arg_type, UnionType):
        if type(None) in get_args(arg_type):
            return True
    return False


_COMPLEX_HANDLERS = {
    # GenericAlias : ,
    _LiteralGenericAlias : parse_literal,
    UnionType : parse_union,
}




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

        if isinstance(self.validator, tuple(_COMPLEX_HANDLERS.keys())):
            return _COMPLEX_HANDLERS[type(self.validator)](self.name, self.validator, values)
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
        allow_unknown = True

    def __init__(self):
        self.args : dict[str,Option] = {}
        args = self.__annotations__
        for arg_name,arg_type in args.items():
            if hasattr(self, arg_name):
                attr = getattr(self, arg_name)
                if isinstance(attr, Option):
                    self.args.append(attr)
                    continue
                default = attr
            else:
                default = None if check_none_default(arg_type) else ...
            self.args[arg_name] = Option(
                name = arg_name,
                abrev = self._config.abrev,
                validator = arg_type,
                positional = True if get_origin(arg_type)==Positional else False,
                default = default
            )
        self._acceptables = self._get_acceptable_arg_names()

    def validate_args(self, args:dict[str,Any]):
        """For more validation on user given args you can override this method.

        After the type validation on args, this method will be called with giving the \
        dictionary of options as `args` parameter.

        in `parse_arguments` all `ValidationError` and `AssertionErrors` caused by \
        this method will be handled and raised as `ValidationError`.

        Args:
            args (dict[str:Any]): dictionary of parsed arguments

        Return:
            it must return the validated dictionary of args
        """
        return args

    def _get_acceptable_arg_names(self) -> dict[str,list[str]]:
        """
        Returns the dictionary of argument names and acceptable argument in \
        command line for them
        """
        acceptables : dict[str, list[str]] = {}
        for arg_name,arg in self.args.items():
            acceptables[arg_name] = [f"--{arg.name}"]
            if arg.abrev:
                i = 0
                abrv = f"-{arg.name[i]}"
                while abrv in acceptables:
                    i += 1
                    abrv += arg.name[i]
                acceptables[arg_name].append(abrv)
        return acceptables

    def _check_acceptable(self, name:str) -> str|None:
        """
        Checks if a given name in command line is acceptable for any argument and \
        returns it's name.

        If name is not found, returns `None`
        """
        for arg_name,abrvs in self._acceptables.items():
            if name in abrvs:
                return arg_name
        return None

    def parse_arguments(self, args:list[str]=sys.argv[1:]):
        i = 0
        results = {}
        arg_counter = {name:arg.maximum for name,arg in self.args.items()}
        to_parse_args = {name:[] for name in self.args.keys()}
        # to_parse_args = {}
        while i < len(args):
            arg = args[i]
            if name:=self._check_acceptable(arg):
                if arg_counter[name] <= 0:
                    raise ValidationError(
                        f"You can use `{name}` option only `{self.args[name].maximum}` times."
                    )
                arg_counter[name] -= 1
                j = i+1
                while  j<len(args)  and  not args[j].startswith("-"):
                    j += 1
                if i+1 == j:
                    if self.args[name].validator == bool:
                        to_send = True
                    else:
                        raise ValidationError(f"`{name}` option needs an argument")
                elif i+2 == j:
                    to_send = args[i+1]
                else:
                    to_send = args[i:j]
                # to_parse_args.setdefault(name, [])
                to_parse_args[name].append(to_send)
                i = j
            elif not self._config.allow_unknown:
                raise ValidationError(f"Unknown argument `{arg}` found")
            else:
                j = i+1
                while  j<len(args)  and  not args[j].startswith("-"):
                    j += 1
                i = j

        for arg_name,values in to_parse_args.items():
            if not values:
                if not self.args[arg_name].required:
                    results[arg_name] = self.args[arg_name].default
                    continue
                else:
                    raise ValidationError(f"Argument `{arg_name}` is required")
            results[arg_name] = self.args[arg_name].parse(*values)


        return self.validate_args(results)


