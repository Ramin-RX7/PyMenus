"""
question module contains the Question class which is used to get a validated answer \
from users easily with less affort
"""

from typing import Any

from ..styles import print
from .validation import ValidationError,Validator



class Question:
    """Question class is used to define structures of how to ask a specific question from user.

    Each question can have multiple options such as name, prompt, default and validators.

    Example:
    --------
    ```python
    >>> def age_validator(raw_input, validated_input, data):
    ...    try:
    ...        age = int(raw_input)
    ...    except ValueError:
    ...        raise ValidationError("Please enter number")
    ...    if age < 18:
    ...        return ValidationError("Only adults can register")
    ...    return age
    >>> age_question = Question("age", "Enter your age:  ", validators=[age_validator])
    >>> age = age_question()
    Enter your age:  asdf
    ValidationError:  Please enter number
    Enter your age:  10
    ValidationError:  Only adults can register
    Enter your age:  19
    # now `age_question` is equal to `19` (of type int since the validator returns int)
    ```
    """

    _names = []
    def __init__(self, name:str, prompt:str, default=None, validators:list[Validator]=None):
        """Question class constructor.

        Args:
            name (str): name of the question which must be unique (this is useful in forms)
            prompt (str): prompt shown to user
            default (Any, optional): a default value when user does not enter anything. If not given, user is required to answer.
            validators (list[Validator], optional): List of validators to be applied to the user answer. Defaults to None.
        """
        assert name not in self.__class__._names, "Name already exists"
        self.name = name
        self.prompt = prompt
        self.validators = validators or []
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
        """When you want to ask the question from user, you easily call the Question object itself.

        Args:
            data (Any, optional): Any data that you need in your validators. Defaults to None.

        Returns:
            Any: Validated response of the user from validators
        """
        while True:
            user_input = input(self.prompt)
            if (not user_input.strip())  and  (self.default is not None):
                return self.default
            validated_value = user_input
            try:
                for validator in self.validators:
                    validated_value = validator(user_input, validated_value, data)
            except ValidationError as e:
                print(f"{str(e)}", color="red")
            else:
                return validated_value
