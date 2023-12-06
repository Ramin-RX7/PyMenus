from .colors import _Colors




class _attribute:
    _prefix = None
    _suffix = "m"
    def __getattribute__(self, __name: str):
        result = super().__getattribute__(__name)
        return self._translate_color(result)

    __getitem__ = __call__ = __getattribute__

    def _translate_color(self, code):
        return f"{self._prefix}{code}m"

    def as_ansi(self, value:int|str):
        if isinstance(value, str):
            if value.startswith(self._prefix):
                return value
            else:
                return getattr(self, value)
                # self._translate_color(super().__getattribute__(value))
        elif isinstance(value, int):
            return self._translate_color(value)
        else:
            raise TypeError("`color` must be either of type `int` or `str`")



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
