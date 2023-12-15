"""
Ultra-CLI `styles` package helps styling terminal outputs.

This package implements:
- Color
- Fore
- Background
- Style
- print
- switch
- switch_default
- reset

which each of them are useful to stylize the terminal output.
But the most useful one is `print` which let's you easily print a colorful text.
"""

from .attributes import (
    Colors,
    Fore,
    Foreground,
    Back,
    Background,
    Style,
)

from .out import (
    print,
    switch,
    switch_default,
    reset,
)
