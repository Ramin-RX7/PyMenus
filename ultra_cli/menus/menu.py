"""
Ultra-CLI `menus.menu` module includes `Menu` class which is a simple class to create menus.
"""

import getpass
from typing import Optional

from pydantic import validator

from ..utils import choice_input
from .base import BaseMenu
from .option import Option



class Menu(BaseMenu):
    """
    Menu object prompts the user to navigate to different sub-menus/options of the app.

    You can add sub_menus and options using `add_submenus` and `add_options`

    Each menu can be run via `execute` method.
    (When user selects a sub-menu, `execute` method of the sub-menu will be called automatically)

    Args (keyword-only):

        title (str): Title will be shown in the list of options

        prompt_text (str): This will be the prompt shown to user when they are in the menu, defaults to title

        sub_menus (list[Menu]): menus you can navigate to from this menu, default: [ ]

        options (list[Option]): options user can choose beside sub-menus, default: [ ]
    """
    title: str
    prompt_text: Optional[str] = None
    sub_menus: list["Menu"] = []
    options: list[Option] = []

    @validator("prompt_text", always=True)
    def _validate_prompt_text(cls, value, values):
        if value is None:
            return values["title"] + "> "
        else:
            return value

    def __repr__(self) -> str:
        menus = [menu.title for menu in self.sub_menus]
        options = [option.title for option in self.options]
        return f"Menu(title='{self.title}', sub_menus={menus}, options={options})"
    def __str__(self) -> str:
        return repr(self)


    def _display_prompt(self) -> bool:
        if not any([self.sub_menus,self.options]):
            print("Empty Menu")
            getpass.getpass("\nPress enter to continue...")
            return False
        if self.sub_menus:
            print("Menus:")
            for i,menu in enumerate(self.sub_menus, 1):
                print(f"   {i}. {menu.title}")
        if self.options:
            print("Options:")
            for i,option in enumerate(self.options, len(self.sub_menus)+1):
                print(f"   {i}. {option.title}")
        print("\n   0. Back\n")
        return True

    def _prompt(self, _display_prompt_return) -> int|None:
        try:
            choice = int(choice_input(
                self.prompt_text,
                [str(i) for i in range(len(self.sub_menus)+len(self.options)+1)]
            ))
        except (EOFError, KeyboardInterrupt):
            return None
        return choice

    def _handle_input(self, _display_prompt_return, number:int) -> tuple[BaseMenu|Option, dict] | None:
        if number == 0:
            return False
        elif number <= len(self.sub_menus):
            sub_menu = self.sub_menus[number-1]
            return (sub_menu, {})
        else:
            option = self.options[number-len(self.sub_menus)-1]
            return (option.function, option.kwargs)


    def add_submenus(self, *sub_menus:"Menu") -> None:
        """
        adds sub-menus to the menu

        Raises:
            TypeError: if sub_menus are not instances of `Menu`
        """
        for menu in sub_menus:
            assert isinstance(menu, Menu), f"sub_menus should be instances of `{self.__class__.__qualname__}`"
            self.sub_menus.append(menu)

    def add_options(self, *options:Option) -> None:
        """Add options to menu options

        Raises:
            TypeError: if options are not instances of `Option`
        """
        for option in options:
            assert isinstance(option, Option), f"options should be instances of `{Option.__qualname__}`"
            self.options.append(option)


    @classmethod
    def parse_dict(cls, dictionary:dict):
        menu = {
            "title"       :  dictionary["title"],
            "prompt_text" :  dictionary.get("prompt_text",None),
            "sub_menus"   :  [cls.parse_dict(submenu) for submenu in dictionary.get("sub_menus",[])],
            "options"     :  [Option(**option) for option in dictionary.get("options",[])]
        }
        return cls(**menu)
