import builtins as _builtins

from .attributes import Fore,Back,Style




def print(*values, color=..., background=..., style=..., sep=" ", end='\n') -> None:
    """prints out the given values decorated with given color/bg/style.

    (You can get list of all colors and styles with: $ python -m rx7 --colors)

    Args:
        color (str, optional): color to use when printing. Defaults to 'default'.
        BG (str, optional): background color of output. Defaults to 'default'.
        style (_type_, optional): style of output text. Defaults to None.
        end (str, optional): last part of print. Defaults to '\n'.
        sep (str, optional): Separator of values in output. Defaults to " ".
    """
    color = "" if color == ... else Fore.as_ansi(color)
    background = "" if background==... else Back.as_ansi(background)
    style = "" if style==... else Style.as_ansi(style)

    values = map(str, values)

    output = f"{style}{color}{background}{sep.join(values)}{end}"

    _builtins.print(output, end="")



def switch(*, color=..., BG=..., style=...) -> None:
    ansi = ""
    if style != ...:
        ansi += f"{Style.as_ansi(style)}"
    if color != ...:
        ansi += f"{Fore.as_ansi(color)}"
    if BG != ...:
        ansi += f"{Back.as_ansi(BG)}"
    _builtins.print(f"{ansi}", end='')


def switch_default() -> None:
    _builtins.print(f'{Style.RESET}', end='')
reset = switch_default
