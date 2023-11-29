import os
import sys
from contextlib import contextmanager


__all__ = (
    "up",
    "down",
    "forward",
    "back",
    "move",
    "SaveCursor",
    "clear_terminal"
)


ESC = '\033'
CE = f'{ESC}['


def stdout(string):
    sys.stdout.write(string)
    sys.stdout.flush()



def up(n:int=1):
    stdout(f"{CE}{n}A")

def down(n:int=1):
    stdout(f"{CE}{n}B")

def forward(n:int=1):
    stdout(f"{CE}{n}C")

def back(n:int=1):
    stdout(f"{CE}{n}D")



def move(x:int=1, y:int=1):
    stdout(f"{CE}{y};{x}H")

def move_rel(x:int=0, y:int=0):
    if x > 0:
        forward(x)
    elif x < 0:
        back(x)
    if y > 0:
        down(y)
    elif y < 0:
        up(y)

def move_home():
    stdout(f'{CE}H')

@contextmanager
def SaveCursor():  # add move to x,y
    try:
        save_position()
        yield
    except Exception as e:
        raise e
    finally:
        restore_position()



def save_position():
    stdout(f"{CE}s")  # f"{ESCC}7"


def restore_position():
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
