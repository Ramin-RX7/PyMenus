"""
`styles.attributes` implements `Color`, `Fore`, `Back` and `Style`.

Each of these are responsible to generate an ANSI code to be printed to terminal and\
 change the output style.

With using these you can manually change the terminal output style but if you want a\
 better API, it's better to use `styles.print` and/or `styles.switch` functions and\
 give them the argument needed (either a normal string or either the attributes of \
 Fore, Back and Style)
"""

from .colors import _Colors




class _attribute:
    _prefix : str = None
    _suffix = "m"
    def __getattribute__(self, __name: str):
        result = super().__getattribute__(__name)
        return self._translate_color(result)

    __getitem__ = __call__ = __getattribute__

    def _translate_color(self, code):
        return f"{self._prefix}{code}m"

    def as_ansi(self, value:int|str):
        """Returns ANSI code of the given attribute

        Args:
            value (int | str): the value that needs to be converted to ANSI

        Raises:
            TypeError: When `value` argument is not `str` and `int`

        Returns:
            str: ANSI string of the given attribute
        """
        if isinstance(value, str):
            if value.startswith(self._prefix):
                return value
            else:
                return getattr(self, value.upper())
                # self._translate_color(super().__getattribute__(value))
        elif isinstance(value, int):
            return self._translate_color(value)
        else:
            raise TypeError("`value` must be either of type `int` or `str`")



class _Back(_Colors, _attribute):
    _prefix = "\x1b[48;5;"


class _Fore(_Colors, _attribute):
    _prefix = "\x1b[38;5;"


class _Style(_attribute):
    _prefix = "\x1b["

    RESET = 0
    BOLD = 1
    BRIGHT = 1
    DIM =  2
    ITALIC = 3
    UNDERLINED = 4
    BLINK = 5
    REVERSE = 7



Colors = _Colors()
Fore = Foreground = _Fore()
Back = Background = _Back()
Style = _Style()
