from typing import Callable,Any,Optional

import rx7 as rx
from pydantic import BaseModel,validator




def default_structure(sub_menus:list["Menu"], options:list["Option"]):
    structure = []
    if sub_menus:
        structure.append("Menus:")
        for i,menu in enumerate(sub_menus, 1):
            structure.append(menu)
    if options:
        structure.append("Options:")
        for i,option in enumerate(options, len(sub_menus)+1):
            structure.append(option)
    structure.append(0)

    return structure


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
    _structure = None


    @validator("prompt_text", always=True)
    def _validate_prompt_text(cls, value, values):
        if value is None:
            return values["title"] + "> "
        else:
            return value

    # @validator("_structure", always=True)
    @classmethod
    def _validate_structure(cls, structure, **values):
        if structure is None:
            return None#default_structure(values['sub_menus'], values['options'])
        else:
            for section in structure:
                if not isinstance(section, (Menu,Option,str,int)):
                    raise TypeError(f"Wrong value in menu structure ({values['title']})")
            return structure

    def __repr__(self) -> str:
        menus = [menu.title for menu in self.sub_menus]
        options = [option.title for option in self.options]
        return f"Menu(title='{self.title}', sub_menus={menus}, options={options})"
    def __str__(self) -> str:
        return repr(self)

    def __setattr__(self, attr, value):
        if attr == "_structure":
            print("set the structure")
            object.__setattr__(self,attr,value)
        else:
            print("set something else")
            super().__setattr__(attr,value)

    def get_user_input(self) -> tuple["Menu"|Callable,dict] | tuple[()]:
        """prompts user input with handling everything related to it.
        (Recommened not to be called externally)

        Returns:
            (tuple) If an argument is selected a tuple of function and kwargs will
            be returned else it will be empty
        """
        if (structure := self._display_prompt()) is False:
            return False
        if (selection := self._prompt(structure)) is None:
            return None
        # if (response := self._handle_input(structure, selection)) is None:
            # return ()
        response = self._handle_input(structure, selection)
        return response

    def _display_prompt(self) -> list[Any]:
        if not any([self.sub_menus,self.options,self._structure]):
            print("Empty Menu")
            rx.getpass("\nPress enter to continue...")
            return False
        structure = self._structure or default_structure(self.sub_menus,self.options)
        if not all([isinstance(section,(Menu,Option,str,int)) for section in structure]):
            raise TypeError(f"Wrong value in menu structure ({self.title})")

        i = 1
        user_input_structure = {}
        for section in structure:
            if isinstance(section, (Menu,Option)):
                print(f"   {i}) {section.title}")
                user_input_structure[i] = section
                i+=1
            elif isinstance(section,str):
                print(section)
            elif isinstance(section,int):
                if section != 0:
                    raise ValueError(f"Invalid structure: `{section}` in menu `{self.title}`")
                print("   0) Back")
                user_input_structure[0] = 0
        return user_input_structure

    def _prompt(self, structure:dict=None) -> int|None:
        print()
        try:
            choice = rx.io.selective_input(
                self.prompt_text,
                choices = [str(i) for i in structure.keys()],
                post_action = int
            )
        except (EOFError, KeyboardInterrupt):
            return None
        return choice

    def _handle_input(self, input_structure:dict[int,Any], number:int) -> tuple[Callable|"Menu", dict] | None:
        if number is None:
            return None
        assert number in input_structure, "Internal error in _prompt() and _handle_input()"
        if number == 0:
            return False
        selected_option = input_structure[number]
        if isinstance(selected_option, Menu):
            return (selected_option, {})
        elif isinstance(selected_option, Option):
            return (selected_option.function, selected_option.kwargs)


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
        if selected_option is False:
            return
        elif selected_option is None:
            exit()

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
        assert (not self._structure), "Can not add submenu when menu is created via structure"
        for menu in sub_menus:
            assert isinstance(menu, Menu), f"sub_menus should be instances of `{self.__class__.__qualname__}`"
            self.sub_menus.append(menu)

    def add_options(self, *options:Option) -> None:
        """Add options to menu options

        Raises:
            TypeError: if options are not instances of `Option`
        """
        assert (not self._structure), "Can not add options when menu is created via structure"
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

    @classmethod
    def parse_structure(cls, title, structure:list["Menu",Option,str,int], prompt_text=None):
        menu =  cls(title=title, prompt_text=prompt_text)
        Menu._validate_structure(structure, title=title)
        menu._structure = structure
        return menu
