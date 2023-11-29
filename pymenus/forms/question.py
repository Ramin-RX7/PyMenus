from typing import Any

from .validation import ValidationError,Validator



class Question:
    _names = []
    def __init__(self, name:str, prompt:str, default=None, validators:list[Validator]=[]):
        assert name not in self.__class__._names, "Name already exists"
        self.name = name
        self.prompt = prompt
        self.validators = validators
        self.default = default

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        assert value not in self.__class__._names, "Name already exists"
        self.__class__._names.append(value)
        self._name = value

    def __call__(self, data=None) -> Any:
        while True:
            user_input = input(self.prompt)
            if (not user_input.strip())  and  (self.default is not None):
                return self.default
            validated_value = user_input
            try:
                for validator in self.validators:
                    validated_value = validator(user_input, validated_value, data)
            except ValidationError:
                print("Invalid Input\n")
            else:
                return validated_value
