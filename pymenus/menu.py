from typing import Callable,Any,Optional

import rx7 as rx
from pydantic import BaseModel,validator





class Option(BaseModel):
    """
    Option object takes a `title` to be shown in the menus and when selected in a menu,
    it will call the given `function` with given `kwargs`
    """
    title:str
    function:Callable
    kwargs: dict[str,Any] = {}



class Menu(BaseModel):
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


    def get_user_input(self) -> tuple["Menu"|Callable,dict] | tuple[()]:
        """prompts user input with handling everything related to it.
        (Recommened not to be called externally)

        Returns:
            (tuple) If an argument is selected a tuple of function and kwargs will
            be returned else it will be empty
        """
        if self._display_prompt() is None:
            return ()
        if (selection := self._prompt()) is None:
            return ()
        if (response := self._handle_input(selection)) is None:
            return ()
        return response

    def _display_prompt(self) -> bool:
        if not any([self.sub_menus,self.options]):
            print("Empty Menu")
            rx.getpass("\nPress enter to continue...")
            return False
        if self.sub_menus:
            print("Menus:")
            for i,menu in enumerate(self.sub_menus, 1):
                print(f"   {i}. {menu.title}")
        if self.options:
            print("Options:")
            for i,option in enumerate(self.options, len(self.sub_menus)+1):
                print(f"   {i}. {option.title}")
        print(f"\n   0. Back\n")
        return True

    def _prompt(self) -> int|None:
        try:
            choice = rx.io.selective_input(
                self.prompt_text,
                choices = [str(i) for i in range(len(self.sub_menus)+len(self.options)+1)],
                post_action = int
            )
        except (EOFError, KeyboardInterrupt):
            return None
        return choice

    def _handle_input(self, number:int) -> tuple[Callable|"Menu", dict] | None:
        if number is None:
            return None
        if number == 0:
            return None
        elif number <= len(self.sub_menus):
            sub_menu = self.sub_menus[number-1]
            return (sub_menu, {})
        else:
            option = self.options[number-len(self.sub_menus)-1]
            return (option.function, option.kwargs)


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
        rx.clear()
        selected_option = self.get_user_input()
        if not selected_option:
            return

        function,defined_kwargs = selected_option
        if isinstance(function, Menu):
            function.execute(**(kwargs if kwargs else defined_kwargs))
        else:
            rx.cls()
            function(**(kwargs if kwargs else defined_kwargs))
            rx.getpass("\nPress enter to continue...")

        self.execute(**kwargs)


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
