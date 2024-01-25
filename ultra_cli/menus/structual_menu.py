"""
Ultra-CLI `menus.structureal_menu` module contains `StructuralMenu` class and it's \
sub-parts (BACK_BUTTON, SEPARATOR) which are used to create a structure based menu.
"""

import getpass
from typing import Callable,Any,Optional

from pydantic import validator

from ..utils import choice_input
from .base import BaseMenu
from .option import Option



BACK_BUTTON = 0
SEPARATOR = "   -------"



class StructuralMenu(BaseMenu):
    """
    Menu object prompts the user to navigate to different sub-menus/options of the app.

    You can add sub_menus and options using `add_submenus` and `add_options`

    Each menu can be run via `execute` method.
    (When user selects a sub-menu, `execute` method of the sub-menu will be called automatically)

    Args (keyword-only):

        title (str): Title will be shown in the list of options

        prompt_text (str): This will be the prompt shown to user when they are in the menu, defaults to title

    """
    title: str
    structure: list
    prompt_text: Optional[str] = None


    @validator("prompt_text", always=True)
    def _validate_prompt_text(cls, value, values):
        if value is None:
            return values["title"] + "> "
        else:
            return value

    @validator("structure")
    def _validate_structure(cls, structure, **values):
        for section in structure:
            if not isinstance(section, (BaseMenu,Option,str,int)):
                raise TypeError(f"Wrong value in menu structure ({values['title']})")
        return structure

    def __repr__(self) -> str:
        return f"StructuralMenu(title='{self.title}', structure=...)"
    def __str__(self) -> str:
        return repr(self)


    def _display_prompt(self) -> list[Any]:
        if not self.structure:
            print("Empty Menu")
            getpass.getpass("\nPress enter to continue...")
            return False
        if not all([isinstance(section,(BaseMenu,Option,str,int)) for section in self.structure]):
            raise TypeError(f"Wrong value in menu structure ({self.title})")

        i = 1
        for section in self.structure:
            if isinstance(section, (BaseMenu,Option)):
                print(f"   {i}) {section.title}")
                i+=1
            elif isinstance(section,str):
                print(section)
            elif isinstance(section,int):
                if section != BACK_BUTTON:
                    raise ValueError(f"Invalid structure: `{section}` in menu `{self.title}`")
                print("   0) Back")
        return self._generate_user_input_structure()

    def _prompt(self, input_structure:dict=None) -> int|None:
        print()
        try:
            choice = int(choice_input(
                self.prompt_text,
                [str(i) for i in input_structure.keys()]
            ))
        except (EOFError, KeyboardInterrupt):
            return None
        return choice or False

    def _handle_input(self, input_structure:dict[int,Any], number:int) -> tuple[Callable|BaseMenu, dict] | None:
        if number is None:
            return None
        assert number in input_structure, "Internal error in _prompt() and _handle_input()"
        if number == 0:
            return False
        selected_option = input_structure[number]
        if isinstance(selected_option, BaseMenu):
            return (selected_option, {})
        elif isinstance(selected_option, Option):
            return (selected_option.function, selected_option.kwargs)


    def _generate_user_input_structure(self):
        i = 1
        user_input_structure = {}
        for section in self.structure:
            if isinstance(section, (BaseMenu,Option)):
                user_input_structure[i] = section
                i+=1
            elif isinstance(section,int):
                user_input_structure[0] = BACK_BUTTON
        return user_input_structure
