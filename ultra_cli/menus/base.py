"""
`menus.base` module defines `BaseMenu` which is the base (Abstract) class for all \
classes that are a menu.
"""

import getpass
from abc import abstractmethod
from typing import Any,final

from pydantic import BaseModel

from ..cursor import clear_terminal
from .option import Option



class BaseMenu(BaseModel):
    @abstractmethod
    def __repr__(self) -> str:
        ...

    @abstractmethod
    def _display_prompt(self) -> Any|None:
        """
        Prints out the menu appearance (like sub-menus,options,etc.).

        It will take no arguments.

        Returns:
            `None` : Exit the app

            `False`: Moves back

            anything else returned by this function will be passed to _prompt()
        """
        ...

    @abstractmethod
    def _prompt(self, _display_prompt_return) -> Any|None:
        """
        Asks for user input.

        This function only takes one argument and that is the return of _display_prompt.

        Returns:
            `None`: close the app.

            `False`: Moves back

            anything else: the return of `_display_prompt()` and this
            function will be sent to `_handle_input()` as arguments
        """
        ...

    @abstractmethod
    def _handle_input(self, _display_prompt_return, _prompt_return) -> Any|None:
        """
        This function handles the user input given in `_prompt()`

        It takes two arguments. First one is the return of
        `_display_prompt()` and the second one is the return of `_prompt()`

        Returns:
            `False`: Moves back

            `None`: Exits the app

            tuple: Must contains two elements.
            First one must be a `_BaseMenu` or `Option` instance.
            Second element is the kwargs of it (dict).
        """
        ...


    @final
    def get_user_input(self):
        """prompts user input with handling everything related to it.
        (Recommened not to be called externally)

        Returns:
            `None`: Exits the app

            `False`: Move back

            tuple: Must contains two elements.
            First one must be a _BaseMenu or Option instance.
            Second element is the kwargs of it (dict).
        """
        if (_display_prompt := self._display_prompt()) in (False,None):
            return _display_prompt
        if (_prompt := self._prompt(_display_prompt)) in (False,None):
            return _prompt
        response = self._handle_input(_display_prompt, _prompt)
        return response


    @final
    def execute(self, **kwargs) -> None:
        """
        This method shoud be called to start the menu.

        All changes applied to the instances such as modifications of
        sub-menu list will be applied in the next call of this method

        Args:
            **kwargs:
                if arguments of the given sub-menus/option have been modified during runtime,
                you can pass them to this method
        """
        clear_terminal()
        selected_option = self.get_user_input()
        if selected_option is False:
            return
        elif selected_option is None:
            exit()
        to_call,defined_kwargs = selected_option
        func_args = kwargs if kwargs else defined_kwargs
        if isinstance(to_call, BaseMenu):
            to_call.execute(**func_args)
        # elif isinstance(to_call, Option):
        elif callable(to_call):
            clear_terminal()
            to_call(**func_args)
            getpass.getpass("\nPress enter to continue...")
        else:
            print(to_call)
            raise TypeError("Invalid type returned by `get_user_input()`")

        self.execute(**kwargs)
