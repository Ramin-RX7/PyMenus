"""
`cursor` is a module that implements different functionalities to interact with\
 terminal cursor.

You can move the cursor in a single direction using:
- up
- down
- forward
- back

You can move the cursor in both axis using:
- move
- move_rel
- move_home

You can save and use the previously saved cursor position using:
- save_position
- restore_postition
- move_temporary

and you can also clear the terminal using `clear_terminal` fuctions.
"""

import os
import sys
from contextlib import contextmanager


__all__ = (
    "up",
    "down",
    "forward",
    "back",
    "move",
    "move_rel",
    "move_home",
    "move_temporary",
    "save_position",
    "restore_position",
    "clear_terminal",
)


ESC = '\033'
CE = f'{ESC}['


def stdout(string):
    sys.stdout.write(string)
    sys.stdout.flush()




def up(n:int=1):
    """Moves terminal cursor to upper rows"""
    stdout(f"{CE}{n}A")


def down(n:int=1):
    """Moves terminal cursor to lower rows"""
    stdout(f"{CE}{n}B")


def forward(n:int=1):
    """Move cursor `n` columns to the right"""
    stdout(f"{CE}{n}C")


def back(n:int=1):
    """Move cursor `n` columns to the left"""
    stdout(f"{CE}{n}D")



def move(x:int=1, y:int=1):
    """Moves the corsor to the given logical position"""
    stdout(f"{CE}{y};{x}H")


def move_rel(x:int=0, y:int=0):
    """Moves the cursor to given position relative to it's current position"""
    if x > 0:
        forward(x)
    elif x < 0:
        back(x)
    if y > 0:
        down(y)
    elif y < 0:
        up(y)


def move_home():
    """Moves the cursor to the first row and column"""
    stdout(f'{CE}H')


@contextmanager
def move_temporary(x=1, y=1):
    """This is a context manager where it saves the current cursor position.

    In the context manager body you can move the cursor but when the manager reaches it's end,
    the cursor will go back to where it was at the start.
    """
    move(x,y)
    try:
        save_position()
        yield
    except Exception as e:
        raise e
    finally:
        restore_position()



def save_position():
    """Saves the current position of the terminal

    Then the `restore_position` function can be used to restore this position
    """
    stdout(f"{CE}s")  # f"{ESCC}7"


def restore_position():
    """Restores the previous saved terminal position using `save_position` function"""
    stdout(f"{CE}u")  # f"{ESCC}8"



def clear_terminal(keep_cursor:bool=False):
    """Clears the terminal environment

    Args:
        keep_cursor (bool, optional): Whether to keep cursor at current position or not. Defaults to False.
    """
    if keep_cursor:
        sys.stdout.write('\033[2J')
        sys.stdout.flush()
        return
    import platform
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')
