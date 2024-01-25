import sys
from types import GenericAlias
from typing import get_origin,Callable,Any

from .exceptions import ValidationError
from .complex_handlers import COMPLEX_HANDLERS
from .utils import check_none_default, clean_class_dict




class Positional:
    def __class_getitem__(cls, item):
        return GenericAlias(cls, item)



class Option:
    """
    `Option` class is used to validate and handle each argument of a ArgumentParser.

    All arguments will be transformed to an `Option` eventually in the ArgumentParser constructor.

    However you can directly use it for more freedom on an argument control during parse.
    """
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
        """
        When an argument needs to be parsed, all of the given values in the terminal\
            will be sent to this function to be validated/cleaned.

        All complex type handlings and validators are done in this method.
        """
        if len(values) > self.maximum:
            raise ValidationError(f"You can use `{self.name}` option only `{self.maximum}` times.")

        if isinstance(self.validator, tuple(COMPLEX_HANDLERS.keys())):
            return COMPLEX_HANDLERS[type(self.validator)](self.name, self.validator, values)
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



class DefaultConfig:
    name = ""
    description = ""
    abrev = True
    allow_unknown = True



class ArgumentParser:
    """
    This class is used to be inherited by user classes to create CLI.

    All the needed arguments must be provided as class attributes with type annotations.

    If an attribute does not provide a default it means they are required.

    Example:

    ```python
    class MyParser(ArgumentParser):
        name : str
        age : int = 18

    parser = MyParser()
    args = parser.parse_arguments()
    # This returns a dictionary of parsed arguments
    ```

    Check more in the examples directory
    """
    Config = DefaultConfig
    def __init__(self):
        self.Config = {
            **clean_class_dict(DefaultConfig),
            **clean_class_dict(self.Config),
        }
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
                abrev = self.Config["abrev"],
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
        """This method is used to parse all given argument and return a dictioanry of \
            the arguments and their corresponding value

        Args:
            args (list[str]): list of given arguments. Defaults to sys.argv[1:].

        Raises:
            ValidationError: this error may be raised due to each of these cases:
            - an option be provided more than the maximum times it has defined
            - if an option needs a value (can not be used as a flag)
            - unknown argument be found (and self.Config.allow_unknown is False)
            - if an argument is required

        Returns:
            dict[str,Any]: parsed arguments as a dictionary
        """
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
            elif not self.Config["allow_unknown"]:
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
