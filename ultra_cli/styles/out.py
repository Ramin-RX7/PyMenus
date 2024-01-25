"""
Ultra-CLI `styles.out` module implements functions used to change the terminal output style.

Functions such as:
- print
- switch
- switch_default (reset)
"""

import builtins as _builtins

from .attributes import Fore,Back,Style




def print(*values, color=..., background=..., style=..., sep=" ", end='\n') -> None:
    """
    prints out the given values decorated with given color, backgroundg and style.

    Args:
        color (str, optional): color to use when printing.
        background (str, optional): background color of output.
        style (_type_, optional): style of output text.
        end (str, optional): last part of print. Defaults to '\n'.
        sep (str, optional): Separator of values in output. Defaults to " ".
    """
    color = "" if color == ... else Fore.as_ansi(color)
    background = "" if background==... else Back.as_ansi(background)
    style = "" if style==... else Style.as_ansi(style)

    values = map(str, values)

    output = f"{style}{color}{background}{sep.join(values)}{end}{Style.RESET}"

    _builtins.print(output, end="")



def switch(*, color=..., BG=..., style=...) -> None:
    """Switches the style of the terminal with given values

    Args:
        color (str, optional): forecolor of the terminal output
        BG (str, optional): background color of the terminal output
        style (str, optional): style of the terinal output
    """
    ansi = ""
    if style != ...:
        ansi += f"{Style.as_ansi(style)}"
    if color != ...:
        ansi += f"{Fore.as_ansi(color)}"
    if BG != ...:
        ansi += f"{Back.as_ansi(BG)}"
    _builtins.print(f"{ansi}", end='')


def switch_default() -> None:
    """Switches the terminal style back to it's default"""
    _builtins.print(f'{Style.RESET}', end='')
reset = switch_default
